interface MistralInput {
    query: string;
    context?: string[];
    parameters?: {
      temperature?: number;    // Default: 0.7
      max_tokens?: number;     // Default: 2048
      top_p?: number;         // Default: 0.95
      top_k?: number;         // Default: 50
    };
    rag_config?: {
      enabled: boolean;       // Default: true
      chunk_size?: number;    // Default: 512
      overlap?: number;       // Default: 50
    };
  }
  