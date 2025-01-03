class ModelWrapper:
    def __init__(self, model_name: str, tokenizer_name: str):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def infer(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        prediction = outputs.logits.argmax(-1).item()
        return prediction
