// src/services/codeLlamaService.js

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const codeLlamaService = {
    generateCode: async (params) => {
        const response = await fetch(`${API_BASE_URL}/api/codellama/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        });
        
        if (!response.ok) {
            throw new Error('Code generation failed');
        }
        
        return response.json();
    },

    getModelInfo: async () => {
        const response = await fetch(`${API_BASE_URL}/api/codellama/info`);
        if (!response.ok) {
            throw new Error('Failed to fetch model info');
        }
        return response.json();
    },
};
