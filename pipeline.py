from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import torch # type: ignore
from abc import ABC, abstractmethod

@dataclass
class ProcessedInput:
    """Data class for storing processed input with metadata"""
    data: Any
    metadata: Dict[str, Any]
    timestamp: float

@dataclass
class ModelOutput:
    """Data class for storing model output with metadata"""
    raw_output: Any
    processed_output: Any
    inference_time: float
    metadata: Dict[str, Any]

class ModelWrapper(ABC):
    """Abstract base class for model wrappers"""
    @abstractmethod
    def infer(self, processed_input: ProcessedInput) -> Any:
        pass

class InferencePipeline:
    def __init__(
        self,
        model_wrapper: ModelWrapper,
        config: Dict[str, Any],
        logger: Optional[logging.Logger] = None
    ):
        """
        Enhanced inference pipeline with configuration and logging.
        
        Args:
            model_wrapper: Model wrapper instance
            config: Configuration dictionary
            logger: Optional logger instance
        """
        self.model_wrapper = model_wrapper
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor(max_workers=config.get("num_workers", 4))
        
        # Initialize cache if enabled
        self.cache = {}
        self.cache_enabled = config.get("caching", {}).get("enabled", False)
        self.cache_size = config.get("caching", {}).get("cache_size", 1000)

    def preprocess_input(self, input_data: Union[str, Dict[str, Any]]) -> ProcessedInput:
        """
        Enhanced preprocessing with input validation and metadata tracking.
        
        Args:
            input_data: Raw input data
            
        Returns:
            ProcessedInput object containing processed data and metadata
        """
        try:
            self.logger.debug(f"Preprocessing input: {input_data[:100]}...")
            
            # Input validation
            if not input_data:
                raise ValueError("Empty input data")
                
            # Convert to string if necessary
            if isinstance(input_data, dict):
                input_text = input_data.get("text", "")
            else:
                input_text = str(input_data)
            
            # Apply preprocessing steps based on config
            processed_data = input_text.strip()
            if self.config.get("preprocessing", {}).get("lowercase", True):
                processed_data = processed_data.lower()
                
            # Create metadata
            metadata = {
                "original_length": len(input_text),
                "processed_length": len(processed_data),
                "preprocessing_steps": ["strip", "lowercase"]
            }
            
            return ProcessedInput(
                data=processed_data,
                metadata=metadata,
                timestamp=time.time()
            )
            
        except Exception as e:
            self.logger.error(f"Preprocessing failed: {str(e)}")
            raise

    def postprocess_output(self, model_output: Any, input_metadata: Dict[str, Any]) -> ModelOutput:
        """
        Enhanced postprocessing with configurable output formatting.
        
        Args:
            model_output: Raw model output
            input_metadata: Metadata from input processing
            
        Returns:
            ModelOutput object containing processed output and metadata
        """
        try:
            self.logger.debug("Postprocessing model output...")
            
            # Convert tensor outputs to numpy/python types if necessary
            if torch.is_tensor(model_output):
                processed_output = model_output.cpu().numpy().tolist()
            else:
                processed_output = model_output
                
            # Format output based on config
            output_format = self.config.get("output", {}).get("format", "dict")
            if output_format == "dict":
                final_output = {
                    "result": processed_output,
                    "confidence": self._calculate_confidence(processed_output)
                }
            else:
                final_output = processed_output
                
            return ModelOutput(
                raw_output=model_output,
                processed_output=final_output,
                inference_time=time.time() - input_metadata["timestamp"],
                metadata={
                    "input_metadata": input_metadata,
                    "output_format": output_format
                }
            )
            
        except Exception as e:
            self.logger.error(f"Postprocessing failed: {str(e)}")
            raise

    def _calculate_confidence(self, output: Any) -> float:
        """Helper method to calculate confidence scores"""
        # Implement confidence calculation logic
        return 1.0

    def process_input(self, input_data: Union[str, Dict[str, Any]]) -> ModelOutput:
        """
        Enhanced main processing pipeline with caching and error handling.
        
        Args:
            input_data: Raw input data
            
        Returns:
            ModelOutput object containing final results
        """
        try:
            # Check cache
            cache_key = str(input_data)
            if self.cache_enabled and cache_key in self.cache:
                self.logger.info("Cache hit, returning cached result")
                return self.cache[cache_key]
            
            # Start timing
            start_time = time.time()
            
            # Preprocessing
            processed_input = self.preprocess_input(input_data)
            
            # Model inference
            model_output = self.model_wrapper.infer(processed_input)
            
            # Postprocessing
            final_output = self.postprocess_output(model_output, processed_input.metadata)
            
            # Update cache
            if self.cache_enabled:
                if len(self.cache) >= self.cache_size:
                    self.cache.pop(next(iter(self.cache)))
                self.cache[cache_key] = final_output
            
            # Log performance metrics
            self.logger.info(f"Processing completed in {time.time() - start_time:.3f}s")
            
            return final_output
            
        except Exception as e:
            self.logger.error(f"Processing pipeline failed: {str(e)}")
            raise

    async def process_input_async(self, input_data: Union[str, Dict[str, Any]]) -> ModelOutput:
        """
        Asynchronous version of process_input for high-throughput scenarios.
        """
        return await self.executor.submit(self.process_input, input_data)
