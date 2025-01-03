// src/hooks/useModelInference.ts
import { useState } from 'react';
import axios from 'axios';

interface InferenceOptions {
    endpoint?: string;
    headers?: Record<string, string>;
}

export const useModelInference = (modelName: string, options?: InferenceOptions) => {
    const [error, setError] = useState<Error | null>(null);

    const runInference = async (input: string) => {
        try {
            const response = await axios.post(
                options?.endpoint || `/api/models/${modelName}/infer`,
                { input },
                { headers: options?.headers }
            );
            return response.data;
        } catch (err) {
            setError(err as Error);
            throw err;
        }
    };

    return { runInference, error };
};
