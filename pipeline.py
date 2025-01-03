class InferencePipeline:
    def __init__(self, model_wrapper: ModelWrapper):
        self.model_wrapper = model_wrapper

    def process_input(self, input_data: str):
        # Preprocess input (if necessary)
        return self.model_wrapper.infer(input_data)
