from transformers import AutoModelForSequenceClassification, AutoTokenizer

class ModelWrapper:
    def __init__(self, model_name: str):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def infer(self, input_text: str):
        inputs = self.tokenizer(input_text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.logits.argmax(-1).item()

# Example: Test model loading and inference
model = ModelWrapper("bert-base-uncased")
print(model.infer("Hello, how are you?"))  # Should print model's prediction (e.g., 0 or 1)


model = ModelWrapper("bert-base-uncased")
input_text = "This is a sample text."
prediction = model.infer(input_text)
print(f"Prediction: {prediction}")

