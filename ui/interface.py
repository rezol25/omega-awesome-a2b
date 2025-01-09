from transformers import AutoModelForCausalLM, AutoTokenizer # type: ignore
import torch # type: ignore
from typing import Dict, Optional, Union
import logging
import time
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMode(Enum):
    STANDARD = "standard"
    CODING = "coding"
    TECHNICAL = "technical"

@dataclass
class ModelConfig:
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    num_return_sequences: int = 1

class Phi2Interface:
    def __init__(self, device: str = "auto", use_cache: bool = True):
        self.model_name = "microsoft/phi-2"
        self.device = device
        self.use_cache = use_cache
        self._initialize_model()
        self.response_cache = {}
        
    def _initialize_model(self):
        """Initialize model with error handling and logging"""
        try:
            logger.info(f"Initializing Phi-2 model on device: {self.device}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map=self.device,
                trust_remote_code=True
            )
            logger.info("Model initialization successful")
        except Exception as e:
            logger.error(f"Model initialization failed: {str(e)}")
            raise

    def generate_response(
        self,
        prompt: str,
        config: Optional[ModelConfig] = None,
        mode: ModelMode = ModelMode.STANDARD,
        stream: bool = False
    ) -> Dict[str, Union[str, float, int]]:
        """
        Generate response with enhanced features and performance metrics
        """
        config = config or ModelConfig()
        
        # Check cache if enabled
        cache_key = f"{prompt}_{mode.value}_{config}"
        if self.use_cache and cache_key in self.response_cache:
            return self.response_cache[cache_key]

        try:
            start_time = time.time()
            
            # Prepare prompt based on mode
            formatted_prompt = self._format_prompt_for_mode(prompt, mode)
            
            # Tokenize input
            inputs = self.tokenizer(
                formatted_prompt, 
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.model.device)

            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=config.max_length,
                    temperature=config.temperature,
                    top_p=config.top_p,
                    top_k=config.top_k,
                    repetition_penalty=config.repetition_penalty,
                    num_return_sequences=config.num_return_sequences,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )

            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Calculate metrics
            generation_time = time.time() - start_time
            token_count = len(outputs[0])
            
            response_data = {
                "text": response_text,
                "generation_time": generation_time,
                "token_count": token_count,
                "mode": mode.value,
                "model_name": self.model_name
            }

            # Cache response if enabled
            if self.use_cache:
                self.response_cache[cache_key] = response_data

            return response_data

        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise

    def _format_prompt_for_mode(self, prompt: str, mode: ModelMode) -> str:
        """Format prompt based on selected mode"""
        mode_prefixes = {
            ModelMode.CODING: "Write code to solve the following: ",
            ModelMode.TECHNICAL: "Provide a technical explanation for: ",
            ModelMode.STANDARD: ""
        }
        return f"{mode_prefixes[mode]}{prompt}"

    def clear_cache(self):
        """Clear the response cache"""
        self.response_cache.clear()
        logger.info("Response cache cleared")

    @property
    def model_info(self) -> Dict:
        """Return model information and current configuration"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "model_parameters": "2.7B",
            "context_window": 2048,
            "cache_enabled": self.use_cache
        }
