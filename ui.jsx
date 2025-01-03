// src/components/BertModelInterface.jsx
import React, { useState, useEffect } from 'react';
import { Button, TextField, Paper, Typography, CircularProgress } from '@mui/material';
import { useModelInference } from '../hooks/useModelInference';

export const BertModelInterface = () => {
    const [input, setInput] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const { runInference } = useModelInference('bert');

    const handleSubmit = async () => {
        try {
            setIsLoading(true);
            const response = await runInference(input);
            setResults(response);
        } catch (error) {
            console.error('Inference failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Paper className="model-interface-container" elevation={3}>
            <Typography variant="h5" className="model-title">
                BERT Model Interface
            </Typography>
            
            <TextField
                fullWidth
                multiline
                rows={4}
                variant="outlined"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Enter text for analysis..."
                className="input-field"
            />

            <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
                disabled={isLoading || !input}
                className="submit-button"
            >
                {isLoading ? <CircularProgress size={24} /> : 'Analyze'}
            </Button>

            {results && (
                <div className="results-container">
                    <Typography variant="h6">Results:</Typography>
                    <pre>{JSON.stringify(results, null, 2)}</pre>
                </div>
            )}
        </Paper>
    );
};
