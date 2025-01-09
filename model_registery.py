# model_registry.py

from typing import Dict, Callable, Any
from models.codellama.codellama_adapter import create_codellama_instance

class ModelRegistry:
    """
    Registry for managing AI models in ai-explorer
    """
    def __init__(self):
        self._models: Dict[str, Callable] = {}

    def register_model(self, model_name: str, model_factory: Callable):
        """
        Register a new model with the registry
        
        Args:
            model_name (str): Unique identifier for the model
            model_factory (Callable): Factory function to create model instance
        """
        if model_name in self._models:
            raise ValueError(f"Model {model_name} is already registered")
        self._models[model_name] = model_factory

    def get_model(self, model_name: str) -> Any:
        """
        Get a model instance by name
        
        Args:
            model_name (str): Name of the model to retrieve
            
        Returns:
            Model instance
        """
        if model_name not in self._models:
            raise KeyError(f"Model {model_name} not found in registry")
        return self._models[model_name]()

    def list_models(self) -> list:
        """
        List all registered models
        
        Returns:
            List of model names
        """
        return list(self._models.keys())

# Create global registry instance
model_registry = ModelRegistry()

def register_models():
    """
    Register all available models
    """
    # Register CodeLlama
    model_registry.register_model("codellama", create_codellama_instance)
    
    # Add other model registrations here as needed
    # model_registry.register_model("other_model", create_other_model_instance)

def get_available_models() -> list:
    """
    Get list of all available models
    
    Returns:
        List of available model names
    """
    return model_registry.list_models()

def get_model(model_name: str) -> Any:
    """
    Get a model instance by name
    
    Args:
        model_name (str): Name of the model to retrieve
        
    Returns:
        Model instance
    """
    return model_registry.get_model(model_name)

# Initialize registry on import
register_models()

# Example usage
if __name__ == "__main__":
    # List available models
    print("Available models:", get_available_models())
    
    # Get CodeLlama instance
    try:
        codellama = get_model("codellama")
        print("Successfully loaded CodeLlama model")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
