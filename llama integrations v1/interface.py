# llava_model.py
from typing import Dict, Any
import torch
from PIL import Image
import base64
import io
from models.base_model import BaseModel  # assuming ai-explorer has this

class LLaVAModel(BaseModel):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(config)
        self.tokenizer = self._load_tokenizer(config)
        
    def _load_model(self, config):
        # Initialize LLaVA model
        from llava.model import LlavaLlamaForCausalLM
        model = LlavaLlamaForCausalLM.from_pretrained(
            config["model_path"],
            device_map="auto",
            torch_dtype=torch.float16
        )
        return model
    
    def _load_tokenizer(self, config):
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained(config["tokenizer_path"])
    
    def _process_image(self, image_data: str) -> Image:
        # Convert base64 to PIL Image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        return image.convert('RGB')
    
    async def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Process input
            image = self._process_image(input_data["image"])
            prompt = input_data["prompt"]
            params = input_data.get("parameters", {})
            
            # Prepare model inputs
            inputs = self.model.prepare_inputs(
                image=image,
                prompt=prompt,
                **params
            )
            
            # Generate response
            with torch.inference_mode():
                output = self.model.generate(**inputs)
                
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            return {
                "response": response,
                "confidence": float(torch.max(output[1]).item()),
                "processing_time": 0.0  # TODO: Add actual timing
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    @property
    def model_info(self) -> Dict[str, Any]:
        return {
            "name": "LLaVA-1.5",
            "version": "1.5",
            "type": "multimodal
