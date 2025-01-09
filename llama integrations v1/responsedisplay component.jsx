const ResponseDisplay: React.FC<ResponseDisplayProps> = ({
    response,
    confidence,
    processingTime
  }) => {
    return (
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Typography variant="body1" gutterBottom>
          {response}
        </Typography>
        <Typography variant="caption" color="textSecondary">
          Confidence: {(confidence * 100).toFixed(2)}% | 
          Processing Time: {processingTime.toFixed(2)}s
        </Typography>
      </Paper>
    );
  };
  