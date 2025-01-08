import React, { useState, useRef } from 'react';
import {
    Button,
    TextField,
    Paper,
    Typography,
    CircularProgress,
    Box,
    Grid,
    Alert,
    Snackbar,
    Card,
    CardContent,
    MenuItem,
    Select,
    InputLabel,
    FormControl,
    Slider,
    IconButton
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import { useModelInference } from '../hooks/useModelInference';

export const EmotiVoiceInterface = () => {
    const [input, setInput] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [emotion, setEmotion] = useState('neutral');
    const [intensity, setIntensity] = useState(0.5);
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef(null);

    const { runInference, isLoading: modelLoading, error: modelError } = useModelInference('mistral');

    const handleSubmit = async () => {
        try {
            setIsLoading(true);
            setError(null);

            // Prepare input data for Mistral
            const response = await runInference({
                query: input,        // The input query
                context: '',         // You can pass any context or document here if needed
                temperature: 0.7     // Modify temperature value for more creative or deterministic responses
            });

            setResults(response);

            // Assuming response contains audioUrl or text for output
            if (response.audioUrl && audioRef.current) {
                audioRef.current.src = response.audioUrl;
            }
        } catch (err) {
            setError('Failed to process the input. Please try again.');
            setOpenSnackbar(true);
        } finally {
            setIsLoading(false);
        }
    };

    const handlePlayPause = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h4" gutterBottom>
                    Mistral Voice Interface
                </Typography>

                <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                        <FormControl fullWidth sx={{ mb: 2 }}>
                            <InputLabel>Emotion</InputLabel>
                            <Select
                                value={emotion}
                                onChange={(e) => setEmotion(e.target.value)}
                                label="Emotion"
                            >
                                <MenuItem value="neutral">Neutral</MenuItem>
                                <MenuItem value="happy">Happy</MenuItem>
                                <MenuItem value="sad">Sad</MenuItem>
                                <MenuItem value="angry">Angry</MenuItem>
                                <MenuItem value="excited">Excited</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <Typography gutterBottom>Emotion Intensity</Typography>
                        <Slider
                            value={intensity}
                            onChange={(_, newValue) => setIntensity(newValue)}
                            min={0}
                            max={1}
                            step={0.1}
                            marks
                            valueLabelDisplay="auto"
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <TextField
                            fullWidth
                            multiline
                            rows={4}
                            variant="outlined"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Enter text to convert to emotional speech..."
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
                >
                    {isLoading || modelLoading ? <CircularProgress size={24} color="inherit" /> : 'Generate Speech'}
                </Button>

                {results && (
                    <Card sx={{ mt: 2 }}>
                        <CardContent>
                            <Typography variant="h6">Audio Output:</Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                <IconButton onClick={handlePlayPause}>
                                    {isPlaying ? <StopIcon /> : <PlayArrowIcon />}
                                </IconButton>
                                <audio ref={audioRef} style={{ display: 'none' }} />
                                <Typography variant="body2" color="textSecondary">
                                    {isPlaying ? 'Playing...' : 'Click to play'}
                                </Typography>
                            </Box>
                            
                            <Typography variant="h6" sx={{ mt: 2 }}>Parameters:</Typography>
                            <Box
                                sx={{
                                    maxHeight: 200,
                                    overflow: 'auto',
                                    backgroundColor: '#f5f5f5',
                                    p: 2,
                                    borderRadius: 1,
                                }}
                            >
                                <pre style={{ margin: 0 }}>{JSON.stringify(results, null, 2)}</pre>
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
                <Alert onClose={() => setOpenSnackbar(false)} severity="error">
                    {error || modelError}
                </Alert>
            </Snackbar>
        </Box>
    );
};
