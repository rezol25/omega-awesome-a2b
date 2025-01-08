// src/config/modelRegistry.js
import { useMistralInference } from '../hooks/mistralInference';

export const modelRegistry = {
    mistral: {
        name: 'Mistral-7B RAG',
        hook: useMistralInference,
        config: {
            maxInputLength: 4096,
            supportedFeatures: ['text', 'documents'],
            defaultParams: {
                temperature: 0.7,
                maxTokens: 2048
            }
        }
    },
    // ... other models
};
