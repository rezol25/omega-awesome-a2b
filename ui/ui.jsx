import React, { useState, useRef, useEffect } from 'react';
import {
    Button, TextField, Paper, Typography, CircularProgress, Box, Grid, 
    Alert, Snackbar, Card, CardContent, MenuItem, Select, InputLabel, 
    FormControl, Slider, IconButton, Tooltip, Chip, useTheme
} from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import SettingsIcon from '@mui/icons-material/Settings';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import MemoryIcon from '@mui/icons-material/Memory';
import { useModelInference } from '../hooks/useModelInference';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/hljs';

export const Phi2Interface = () => {
    const theme = useTheme();
    const [input, setInput] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [mode, setMode] = useState('standard');
    const [temperature, setTemperature] = useState(0.7);
    const [maxLength, setMaxLength] = useState(1024);
    const [showAdvanced, setShowAdvanced] = useState(false);

    const { runInference, isLoading: modelLoading, error: modelError } = useModelInference('phi-2');

    const handleSubmit = async () => {
        try {
            setIsLoading(true);
            setError(null);

            const response = await runInference({
                prompt: input,
                mode: mode,
                config: {
                    temperature,
                    max_length: maxLength,
                    top_p: 0.9,
                    top_k: 50,
                }
            });

            setResults(response);
        } catch (err) {
            setError('Failed to process input. Please try again.');
            setOpenSnackbar(true);
        } finally {
            setIsLoading(false);
        }
    };

    const renderOutput = () => {
        if (!results) return null;

        if (mode === 'coding') {
            return (
                <SyntaxHighlighter 
                    language="python" 
                    style={tomorrow}
                    customStyle={{
                        borderRadius: theme.shape.borderRadius,
                        padding: theme.spacing(2)
                    }}
                >
                    {results.text}
                </SyntaxHighlighter>
            );
        }

        return (
            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {results.text}
            </Typography>
        );
    };

    return (
        <Box sx={{ maxWidth: 1000, mx: 'auto', p: 2 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
                <Grid sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <MemoryIcon sx={{ mr: 1 }} />
                    <Typography variant="h4">Phi-2 Interface</Typography>
                2{'}'}&gt;
                    <Grid item xs={12} md={6}>
                        <FormControl fullWidth>
                            <InputLabel>Mode</InputLabel>
                            <Select
                                value={mode}
                                onChange={(e) => setMode(e.target.value)}
                                label="Mode"
                                startAdornment={<CodeIcon sx={{ mr: 1 }} />}
                            >
                                <MenuItem value="standard">Standard</MenuItem>
                                <MenuItem value="coding">Coding</MenuItem>
                                <MenuItem value="technical">Technical</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <Button
                            startIcon={<SettingsIcon />}
                            onClick={() => setShowAdvanced(!showAdvanced)}
                            variant="outlined"
                            fullWidth
                        >
                            Advanced Settings
                        </Button>
                    </Grid>

                    {showAdvanced && (
                        <>
                            <Grid item xs={12} md={6}>
                                <Typography gutterBottom>Temperature</Typography>
                                <Slider
                                    value={temperature}
                                    onChange={(_, value) => setTemperature(value)}
                                    min={0.1}
                                    max={1.0}
                                    step={0.1}
                                    marks
                                    valueLabelDisplay="auto"
                                />
                            </Grid>

                            <Grid item xs={12} md={6}>
                                <Typography gutterBottom>Max Length</Typography>
                                <Slider
                                    value={maxLength}
                                    onChange={(_, value) => setMaxLength(value)}
                                    min={256}
                                    max={2048}
                                    step={256}
                                    marks
                                    valueLabelDisplay="auto"
                                />
                            </Grid>
                        </>
                    )}

                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            multiline
                            rows={6}
                            variant="outlined"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder={mode === 'coding' ? 
                                "Describe the code you want to generate..." : 
                                "Enter your prompt..."}
                            sx={{ mb: 2 }}
                        />
                    </Grid>
                </Grid>

                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                    disabled={isLoading || !input}
                    fullWidth
                    sx={{ mb: 2 }}
                    startIcon={<AutoFixHighIcon />}
                >
                    {isLoading || modelLoading ? 
                        <CircularProgress size={24} color="inherit" /> : 
                        'Generate Response'}
                </Button>

                {results && (
                    <Card sx={{ mt: 2 }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                                <Typography variant="h6">Output:</Typography>
                                <Chip 
                                    label={`${results.generation_time.toFixed(2)}s`}
                                    color="primary"
                                    variant="outlined"
                                    size="small"
                                />
                            </Box>
                            
                            {renderOutput()}

                            <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                                <Chip 
                                    label={`Tokens: ${results.token_count}`}
                                    variant="outlined"
                                    size="small"
                                />
                                <Chip 
                                    label={`Mode: ${results.mode}`}
                                    variant="outlined"
                                    size="small"
                                />
                            </Box>
                        </CardContent>
                    </Card>
                )}
            </Paper>

            <Snackbar
                open={openSnackbar}
                autoHideDuration={6000}
                onClose={() => setOpenSnackbar(false)}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert 
                    onClose={() => setOpenSnackbar(false)} 
                    severity="error"
                    variant="filled"
                >
                    {error || modelError}
                </Alert>
            </Snackbar>
        </Box>
    );
};
