import os
import copy
import math
import warnings
import shutil
from functools import partial

import torch

from .model import load_pretrained_model
from .model.processor import Videollama3Processor
from .mm_utils import load_images, process_images, load_video, process_video, tokenizer_multimodal_token, get_model_name_from_path, KeywordsStoppingCriteria
from .constants import NUM_FRAMES, DEFAULT_IMAGE_TOKEN, DEFAULT_VIDEO_TOKEN, MODAL_INDEX_MAP, STREAM_START_TOKEN, STREAM_END_TOKEN


def disable_torch_init():
    """
    Disable the redundant torch default initialization to accelerate model creation.
    """
    import torch
    setattr(torch.nn.Linear, "reset_parameters", lambda self: None)
    setattr(torch.nn.LayerNorm, "reset_parameters", lambda self: None)
    

def model_init(model_path=None, **kwargs):
    model_path = "DAMO-NLP-SG/VideoLLaMA2-7B" if model_path is None else model_path
    model_name = get_model_name_from_path(model_path)
    tokenizer, model, processor, context_len = load_pretrained_model(model_path, None, model_name, **kwargs)

    if tokenizer.pad_token is None and tokenizer.unk_token is not None:
        tokenizer.pad_token = tokenizer.unk_token

    aspect_ratio = model.config.image_aspect_ratio if hasattr(model.config, "image_aspect_ratio") else "pad"
    image_size = model.config.image_size if hasattr(model.config, "image_size") else 384
    # NOTE: If num_frames is None, the frame sampling mode is "fps". If num_frames is not None, the frame sampling mode is "uniform". 
    num_frames = model.config.num_frames

    processor = {
        'image': load_images,
        'video': load_video,
        'text':  None
    }

    return model, processor, tokenizer


def mm_infer(images_or_videos, instruct, model, tokenizer, modal='video', **kwargs):
    """inference api of VideoLLaMA2 for video understanding.

    Args:
        model: VideoLLaMA2 model.
        images_or_videos (torch.Tensor): image tensor (1, C, H, W) / video tensor (T, C, H, W).
        instruct (str): text instruction for understanding video.
        tokenizer: tokenizer.
        do_sample (bool): whether to sample.
        modal (str): inference modality.
    Returns:
        str: response of the model.
    """
    if modal == 'image':
        modal_token = DEFAULT_IMAGE_TOKEN
        images = images_or_videos
        timestamps = None
    elif modal == 'video':
        modal_token = DEFAULT_VIDEO_TOKEN
        images, timestamps = images_or_videos
    elif modal == 'text':
        modal_token = ''
    else:
        raise ValueError(f"Unsupported modal: {modal}")

    vlprocessor = Videollama3Processor(model.get_vision_encoder().image_processor, tokenizer)
    vlprocessor.tokenizer.add_tokens([DEFAULT_IMAGE_TOKEN, STREAM_START_TOKEN, STREAM_END_TOKEN], special_tokens=True)

    model.config.image_token_index = vlprocessor.tokenizer.convert_tokens_to_ids(DEFAULT_IMAGE_TOKEN)

    # 1. text preprocess (tag process & generate prompt).
    if isinstance(instruct, str):
        messages = [{'role': 'user', 'content': instruct}]
    elif isinstance(instruct, list):
        messages = copy.deepcopy(instruct)
    else:
        raise ValueError(f"Unsupported type of instruct: {type(instruct)}")

    if all(not modal_token in message["content"] for message in messages):
        warnings.warn(f"Image tag not found in the conversation, add it automatically at the beginning!")
        messages[0]["content"] = modal_token + messages[0]["content"]

    converted_messages = []
    for message in messages:
        chunks = message["content"].split(modal_token)
        converted_messages.append({
            "role": "user",
            "content": []
        })

        for chunk_idx in range(1, 2 * len(chunks)):
            if chunk_idx % 2 == 1:
                chunk = chunks[chunk_idx // 2].strip()
                converted_messages[-1]["content"].append({"type": "text",  "text": chunk}) if chunk else None
            else:
                if modal == 'image':
                    converted_messages[-1]["content"].append({"type": "image"})
                elif modal == 'video':
                    converted_messages[-1]["content"].append({"type": "video", "num_frames": len(images), "time": timestamps})

    messages = converted_messages

    # 2. vision preprocess (load & transform image or video).
    if model.config.model_type in ['videollama3_mistral', 'videollama3_mixtral']:
        system_message = [
            {'role': 'system', 'content': (
            """<<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature."""
            """\n"""
            """If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>""")
            }
        ]
    else:
        system_message = []

    # TODO: attention mask?
    messages = system_message + messages
    data_dict = vlprocessor(
        images=images,
        text=messages,
        image_downsampling=model.config.spatial_merge_size,
        return_tensors="pt",
    )

    torch_dtype = model.config.torch_dtype if hasattr(model.config, "torch_dtype") else torch.float16

    images = [x.to(torch_dtype).cuda(non_blocking=True) for x in data_dict["images"]]
    grid_thws = [x.cuda(non_blocking=True) for x in data_dict["grid_thws"]]

    # 3. generate response according to visual signals and prompts. 
    keywords = [tokenizer.eos_token]
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, data_dict["input_ids"])

    do_sample = kwargs.get('do_sample', False)
    temperature = kwargs.get('temperature', 0.2 if do_sample else 0.0)
    top_p = kwargs.get('top_p', 0.9)
    max_new_tokens = kwargs.get('max_new_tokens', 2048)

    with torch.inference_mode():
        output_ids = model.generate(
            # input_ids,
            # attention_mask=attention_masks,
            # images=images,
            data_dict["input_ids"].cuda(),
            attention_mask=data_dict["attention_mask"].cuda(),
            images=[(modal, images, grid_thws)],
            do_sample=do_sample,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            use_cache=True,
            stopping_criteria=[stopping_criteria],
            pad_token_id=tokenizer.eos_token_id,
        )

    outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()

    return outputs
