// components/LLaVAInterface.tsx
import React, { useState } from 'react';
import { Button, TextField, Paper, Grid, Typography, CircularProgress } from '@mui/material';
import ImageUpload from './ImageUpload';
import ResponseDisplay from './ResponseDisplay';

const LLaVAInterface: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Handles image upload
  const handleImageUpload = (uploadedImage: string) => {
    setImage(uploadedImage);
    setResponse(null); // Clear previous response on new upload
  };

  // Handles query submission
  const handleSubmit = async () => {
    if (!image || !prompt) return;

    setLoading(true);
    try {
      const result = await fetch('/process_query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image, prompt }),
      }).then((res) => res.json());

      setResponse(result);
    } catch (error) {
      console.error('Error fetching response:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, m: 2 }}>
      <Typography variant="h5" gutterBottom>
        LLaVA-1.5 Visual Question Answering
      </Typography>

      <Grid container spacing={3}>
        {/* Left side - Image Upload */}
        <Grid item xs={12} md={6}>
          <ImageUpload 
            onUpload={handleImageUpload}
            currentImage={image}
          />
        </Grid>

        {/* Right side - Prompt Input */}
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            label="Ask about the image"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            sx={{ mb: 2 }}
          />

          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            disabled={!image || !prompt || loading}
            fullWidth
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Response'}
          </Button>
        </Grid>

        {/* Response Display */}
        {response && (
          <Grid item xs={12}>
            <ResponseDisplay 
              response={response.response}
              confidence={response.confidence}
              processingTime={response.processing_time}
            />
          </Grid>
        )}
      </Grid>
    </Paper>
  );
};

export default LLaVAInterface;
