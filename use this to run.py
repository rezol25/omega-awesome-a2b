import torch
from torch.utils.data import DataLoader
from transformers import CLIPProcessor
from PIL import Image
import os
from typing import Dict
import logging

class MultiModalDataset(torch.utils.data.Dataset):
    """
    A dataset loader that processes image-text pairs for multi-modal learning.
    Supports understanding, generation, and unified processing.
    """
    def __init__(self, 
                 image_dir: str,
                 text_file: str,
                 processor: CLIPProcessor,
                 mode: str = 'unified',
                 max_length: int = 77,
                 image_size: Tuple[int, int] = (224, 224)):
        """
        Args:
            image_dir (str): Directory containing images.
            text_file (str): Path to text annotations.
            processor (CLIPProcessor): The processor for transforming text and images.
            mode (str): Mode of operation ('unified', 'understanding', or 'generation').
            max_length (int): Maximum length of text for tokenization.
            image_size (Tuple[int, int]): Image resize dimensions.
        """
        self.mode = mode
        self.max_length = max_length
        self.image_size = image_size

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Validate and load data
        self._validate_paths(image_dir, text_file)
        self.processor = processor
        self.image_paths, self.texts = self._load_data(image_dir, text_file)

    def _validate_paths(self, image_dir: str, text_file: str) -> None:
        """Validate image and text file paths."""
        if not os.path.exists(image_dir):
            raise ValueError(f"Image directory {image_dir} does not exist.")
        if not os.path.exists(text_file):
            raise ValueError(f"Text file {text_file} does not exist.")

    def _load_data(self, image_dir: str, text_file: str) -> Tuple[list, list]:
        """Load image-text data pairs."""
        image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        with open(text_file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f.readlines()]

        if len(image_paths) != len(texts):
            raise ValueError("Number of images and text entries must match.")
        
        return image_paths, texts

    def __len__(self):
        """Returns the total number of samples."""
        return len(self.image_paths)

    def _process_image(self, image_path: str) -> Image.Image:
        """Open and resize the image."""
        try:
            image = Image.open(image_path).convert("RGB")
            image = image.resize(self.image_size)
            return image
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {e}")
            raise

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """
        Returns the processed image and text for the given index, 
        adjusted to the mode (unified, understanding, generation).
        """
        image = self._process_image(self.image_paths[idx])
        text = self.texts[idx]

        # Process image and text according to mode
        inputs = self.processor(
            text=text,
            images=image,
            return_tensors="pt",
            padding="max_length",
            max_length=self.max_length,
            truncation=True
        )
        
        # Return the processed data, depending on the mode
        if self.mode == 'generation':
            # Add specific generation-related processing (e.g., noise)
            inputs['noised_images'] = self._add_noise(inputs['pixel_values'])
        elif self.mode == 'unified':
            inputs['original_images'] = inputs['pixel_values'].clone()
        
        # Return the data as a dictionary
        return {k: v.squeeze(0) for k, v in inputs.items()}

    def _add_noise(self, image: torch.Tensor, noise_level: float = 0.1) -> torch.Tensor:
        """Adds Gaussian noise for generative tasks."""
        noise = torch.randn_like(image) * noise_level
        return image + noise


def create_dataloader(
    image_dir: str,
    text_file: str,
    batch_size: int = 16,
    mode: str = 'unified'
) -> DataLoader:
    """Create a DataLoader for multi-modal data."""
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
    dataset = MultiModalDataset(
        image_dir=image_dir,
        text_file=text_file,
        processor=processor,
        mode=mode
    )
    
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )


# Example usage:
dataloader = create_dataloader(
    image_dir="path_to_images", 
    text_file="path_to_texts.txt", 
    batch_size=16, 
    mode='unified'
)

# Iterate through batches
for batch in dataloader:
    # Access different modalities
    images = batch['pixel_values']
    text_inputs = batch['input_ids']
    attention_mask = batch['attention_mask']
    # Process with your model...
