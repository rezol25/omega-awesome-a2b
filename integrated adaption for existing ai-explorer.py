## Updated Phi-2 Inference Code for Integration with AI Explorer
## This script integrates the Phi-2 model into the AI Explorer interface.

from ast import Import
import React, { useState, useEffect } from 'react'; # type: ignore # type: ignore
import { Button, TextField, Paper, Typography, CircularProgress } from '@mui/material'; # type: ignore
import { useModelInference } from '../hooks/useModelInference'; # type: ignore

Import const Phi2ModelInterface = () => { # type: ignore
    const [input, setInput] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const { runInference } = useModelInference('phi-2');

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
                Phi-2 Model Interface
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
    )
}