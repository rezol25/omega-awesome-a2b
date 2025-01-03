// src/components/ErrorDisplay.jsx
export const ErrorDisplay = ({ error }) => (
    <Paper className="error-container" elevation={3}>
        <Typography color="error">
            Error: {error.message}
        </Typography>
    </Paper>
);
