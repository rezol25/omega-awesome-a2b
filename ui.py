# phi2_explorer_ui.py
import gradio as gr # type: ignore
from phi2_explorer import Phi2ExplorerIntegration # type: ignore

class Phi2ExplorerUI:
    def __init__(self):
        self.model = Phi2ExplorerIntegration()
        
    def create_interface(self):
        with gr.Blocks(title="Phi-2 AI Explorer Interface") as interface:
            gr.Markdown("# Phi-2 Model Explorer")
            gr.Markdown("### A powerful 2.7B parameter model for text generation and reasoning")
            
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(
                        label="Input Prompt",
                        placeholder="Enter your prompt here...",
                        lines=5
                    )
                    
                    with gr.Row():
                        temperature = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=0.7,
                            label="Temperature"
                        )
                        max_length = gr.Slider(
                            minimum=50,
                            maximum=1000,
                            value=200,
                            step=50,
                            label="Max Length"
                        )
                    
                    generate_btn = gr.Button("Generate")
                    
                with gr.Column():
                    output_text = gr.Textbox(
                        label="Generated Output",
                        lines=10,
                        interactive=False
                    )
                    
            generate_btn.click(
                fn=self.generate_response,
                inputs=[input_text, temperature, max_length],
                outputs=[output_text]
            )
            
            # Add examples
            gr.Examples(
                examples=[
                    ["Explain quantum computing to a high school student.",],
                    ["Write a short story about a robot learning to paint.",],
                    ["What are the key principles of sustainable architecture?",]
                ],
                inputs=[input_text]
            )
            
            # Add model information
            with gr.Accordion("Model Information", open=False):
                gr.Markdown("""
                - **Model**: Phi-2
                - **Size**: 2.7B parameters
                - **Context Window**: 2048 tokens
                - **License**: MIT (research)
                - **Capabilities**: Text generation, reasoning, coding
                """)
        
        return interface
    
    def generate_response(self, prompt, temperature, max_length):
        try:
            response = self.model.generate_text(
                prompt,
                temperature=temperature,
                max_length=max_length
            )
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Launch the interface
if __name__ == "__main__":
    ui = Phi2ExplorerUI()
    interface = ui.create_interface()
    interface.launch(share=True)
