// components/LLaVAInterface.tsx
import React, { useState, useRef } from 'react';
import { Button, TextField, Paper, Grid, Typography } from '@mui/material';

const LLaVAInterface: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Main component structure
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
            {loading ? 'Processing...' : 'Generate Response'}
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
