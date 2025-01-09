import { validateRequest } from '../../../utils/validation';

router.post(async (req, res) => {
  try {
    // Validate request
    const validation = validateRequest(req);
    if (!validation.success) {
      return res.status(400).json({ error: validation.error });
    }

    upload.single('image')(req as any, res as any, async (err) => {
      if (err) {
        if (err.code === 'LIMIT_FILE_SIZE') {
          return res.status(400).json({ error: 'File size exceeds 5MB limit' });
        }
        return res.status(400).json({ error: 'File upload error' });
      }

      try {
        const { prompt, parameters } = req.body;
        const imageFile = (req as any).file;
        
        // Validate parameters
        const parsedParams = JSON.parse(parameters);
        if (!isValidParameters(parsedParams)) {
          return res.status(400).json({ error: 'Invalid parameters' });
        }

        let image = null;
        if (imageFile) {
          image = await sharp(imageFile.buffer)
            .resize(336, 336, { fit: 'contain' })
            .toBuffer();
        }

        const response = await model.generate(prompt, image, parsedParams);
        res.status(200).json({ response });
      } catch (error) {
        console.error('Processing error:', error);
        res.status(500).json({ error: 'Error processing request' });
      }
    });
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
