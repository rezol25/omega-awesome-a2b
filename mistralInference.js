// src/hooks/mistralInference.js
import { useState, useCallback } from 'react';

const MISTRAL_ENDPOINT = process.env.REACT_APP_MISTRAL_ENDPOINT;

export const useMistralInference = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const runInference = useCallback(async ({
        query,
        context = [],
        temperature = 0.7,
        maxTokens = 2048
    }) => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(MISTRAL_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query,
                    context,
                    parameters: {
                        temperature,
                        max_tokens: maxTokens,
                        top_p: 0.95,
                        top_k: 50,
                    },
                    rag_config: {
                        enabled: true,
                        chunk_size: 512,
                        overlap: 50,
                        similarity_threshold: 0.7
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            return {
                generated_text: data.response,
                retrieved_contexts: data.contexts,
                metadata: {
                    processing_time: data.processing_time,
                    tokens_used: data.usage.total_tokens,
                    relevant_docs: data.retrieved_documents
                }
            };
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        runInference,
        isLoading,
        error
    };
};
