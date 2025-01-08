# Updated Phi-2 Inference Code
import torch # type: ignore
from transformers import AutoModelForCausalLM, AutoTokenizer # type: ignore
import logging

class Phi2ExplorerIntegration:
    def __init__(self, model_name="microsoft/phi-2", device=None):
        """Initialize Phi-2 model with proper error handling."""
        try:
            self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
            logging.info(f"Using device: {self.device}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.model.to(self.device)
            
        except Exception as e:
            logging.error(f"Error initializing Phi-2: {str(e)}")
            raise

    def generate_text(self, prompt, max_length=200, temperature=0.7, top_k=50):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=max_length,
                    temperature=temperature,
                    top_k=top_k,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logging.error(f"Error generating text: {str(e)}")
            return f"Error: {str(e)}"

# Test the implementation
def test_phi2():
    try:
        model = Phi2ExplorerIntegration()
        test_prompt = "Explain what makes quantum computing different from classical computing:"
        response = model.generate_text(test_prompt)
        print(f"Prompt: {test_prompt}\nResponse: {response}")
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_phi2()
