Phi-2 Benchmark Documentation
Model Specifications
Model Size: 2.7 billion parameters
Context Window: 2048 tokens
Architecture: Transformer-based
Resource Requirements
VRAM Requirement: 3–4 GB
Input/Output Format
Input Format: Text (e.g., natural language prompts, queries)
Output Format: Text (e.g., summaries, completions, or reasoning chains)
License
Type: MIT License (for research purposes)
Benchmark Examples
1. Language Understanding
Task: Zero-shot Question Answering (Natural Questions)
Dataset: Natural Questions (NQ)
Metric: Exact Match (EM) Score
Performance:

Phi-2 achieves 43.7% EM, surpassing earlier models of similar size by 5-10%.
2. Text Generation
Task: Story Continuation
Dataset: WritingPrompts
Metric: Perplexity and Human Evaluation Scores
Performance:

Perplexity: 9.2
Human Evaluation: Rated 85% natural compared to ground truth stories.
3. Code Generation
Task: Python Code Completion
Dataset: HumanEval Benchmark
Metric: Pass@1 (single-attempt accuracy)
Performance:

Phi-2 achieves 36.8% Pass@1, comparable to larger 6B models.
4. Reasoning
Task: Logical Reasoning in Text
Dataset: GSM8K (Grade School Math Problems)
Metric: Accuracy
Performance:

Accuracy: 21.5%, with improvements when fine-tuned on reasoning-specific datasets.
Performance Metrics Summary
Task	Metric	Performance	Notes
Question Answering	EM Score	43.7%	Outperforms similar-sized models.
Story Continuation	Perplexity	9.2	Generates coherent and natural text.
Code Generation	Pass@1	36.8%	Matches performance of larger models.
Logical Reasoning	Accuracy	21.5%	Room for improvement on math tasks.