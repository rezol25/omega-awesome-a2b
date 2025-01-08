// src/hooks/useModelInference.js
import { modelRegistry } from '../config/modelRegistry';

export const useModelInference = (modelName) => {
    if (!modelRegistry[modelName]) {
        throw new Error(`Model ${modelName} not found in registry`);
    }

    const { hook: useModelHook } = modelRegistry[modelName];
    return useModelHook();
};
