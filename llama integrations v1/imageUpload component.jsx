const ImageUpload: React.FC<ImageUploadProps> = ({ onUpload, currentImage }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
  
    return (
      <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', minHeight: 200 }}>
        {currentImage ? (
          <img 
            src={currentImage} 
            alt="Uploaded"
            style={{ maxWidth: '100%', maxHeight: 300 }}
          />
        ) : (
          <Button
            variant="outlined"
            onClick={() => fileInputRef.current?.click()}
          >
            Upload Image
          </Button>
        )}
        <input
          type="file"
          hidden
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="image/*"
        />
      </Paper>
    );
  };
  