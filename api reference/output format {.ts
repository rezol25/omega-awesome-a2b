interface MistralOutput {
    generated_text: string;
    retrieved_contexts: string[];
    metadata: {
      processing_time: number;
      tokens_used: number;
      relevant_docs: number;
    };
  }
  