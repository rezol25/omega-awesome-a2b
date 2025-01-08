import torch # type: ignore
from torch.utils.data import Dataset, DataLoader # type: ignore
from transformers import CLIPProcessor # type: ignore
from PIL import Image # type: ignore
import os
import logging
from typing import Dict, List, Tuple, Optional
import numpy as np # type: ignore

class EnhancedMultiModalDataset(Dataset):
    """
    Enhanced MultiModal Dataset loader supporting both MLLM and diffusion-style processing
    """
    def __init__(self, 
                 image_dir: str,
                 text_file: str,
                 processor: CLIPProcessor,
                 mode: str = 'unified',
                 max_length: int = 77,
                 image_size: Tuple[int, int] = (224, 224),
                 augment: bool = True):
        """
        Args:
            image_dir: Directory containing images
            text_file: Path to text annotations
            processor: CLIP processor for initial processing
            mode: 'unified', 'understanding', or 'generation'
            max_length: Maximum text length
            image_size: Target image size
            augment: Whether to use data augmentation
        """
        super().__init__()
        self.mode = mode
        self.max_length = max_length
        self.image_size = image_size
        self.augment = augment
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Validate and load data
        self._validate_paths(image_dir, text_file)
        self.processor = processor
        self.image_paths, self.texts = self._load_data(image_dir, text_file)
        
        # Setup augmentation if needed
        if self.augment:
            self.augmentation = self._setup_augmentation()

    def _validate_paths(self, image_dir: str, text_file: str) -> None:
        """Validate input paths"""
        if not os.path.exists(image_dir):
            raise ValueError(f"Image directory {image_dir} does not exist")
        if not os.path.exists(text_file):
            raise ValueError(f"Text file {text_file} does not exist")

    def _load_data(self, image_dir: str, text_file: str) -> Tuple[List[str], List[str]]:
        """Load and validate data pairs"""
        image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        with open(text_file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f.readlines()]
        
        if len(image_paths) != len(texts):
            raise ValueError("Number of images and text entries must match")
            
        return image_paths, texts

    def _setup_augmentation(self):
        """Setup data augmentation pipeline"""
        try:
            import albumentations as A # type: ignore
            return A.Compose([
                A.RandomResizedCrop(*self.image_size),
                A.HorizontalFlip(p=0.5),
                A.RandomBrightnessContrast(p=0.2),
            ])
        except ImportError:
            self.logger.warning("Albumentations not installed. Skipping augmentation.")
            self.augment = False
            return None

    def _process_image(self, image_path: str) -> Image.Image:
        """Process and validate image"""
        try:
            image = Image.open(image_path).convert("RGB")
            if self.augment and self.augmentation:
                image = self.augmentation(image=np.array(image))['image']
                image = Image.fromarray(image)
            return image
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """
        Get item based on mode (understanding/generation/unified)
        """
        image = self._process_image(self.image_paths[idx])
        text = self.texts[idx]

        # Process based on mode
        if self.mode == 'understanding':
            inputs = self.processor(
                text=text,
                images=image,
                return_tensors="pt",
                padding="max_length",
                max_length=self.max_length,
                truncation=True
            )
        elif self.mode == 'generation':
            # Additional processing for generation tasks
            inputs = self.processor(
                text=text,
                images=image,
                return_tensors="pt",
                padding="max_length",
                max_length=self.max_length,
                truncation=True
            )
            # Add noise for diffusion-based training
            inputs['noised_images'] = self._add_noise(inputs['pixel_values'])
        else:  # unified mode
            inputs = self.processor(
                text=text,
                images=image,
                return_tensors="pt",
                padding="max_length",
                max_length=self.max_length,
                truncation=True
            )
            inputs['original_images'] = inputs['pixel_values'].clone()

        return {k: v.squeeze(0) for k, v in inputs.items()}

    def _add_noise(self, image: torch.Tensor, noise_level: float = 0.1) -> torch.Tensor:
        """Add Gaussian noise for diffusion training"""
        noise = torch.randn_like(image) * noise_level
        return image + noise

# Example usage:
def create_dataloader(
    image_dir: str,
    text_file: str,
    batch_size: int = 16,
    mode: str = 'unified'
) -> DataLoader:
    """Create a dataloader with specified configuration"""
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
    dataset = EnhancedMultiModalDataset(
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