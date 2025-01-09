# LLaVA Integration Setup Guide for AI Explorer

## System Requirements

### Hardware Requirements
- NVIDIA GPU with 16GB+ VRAM (24GB recommended for optimal performance)
- 32GB System RAM minimum
- 50GB free disk space

### Software Prerequisites
- Ubuntu 20.04 LTS or later (recommended) / Windows 10/11 with WSL2
- CUDA 11.7 or later
- Python 3.8+
- Node.js 16+
- Git LFS
- Docker (optional)

## Installation Steps

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/omega-awesome-a2a/ai-explorer.git
cd ai-explorer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
2. Model Setup
bash
Copy
# Create model directory
mkdir -p models/llava

# Download LLaVA model weights (7B version)
python scripts/download_llava.py --model-size 7b

# Verify model installation
python scripts/verify_llava.py
3. Configuration
Create .env file in project root:

env
Copy
LLAVA_MODEL_PATH=./models/llava-1.5-7b
CUDA_VISIBLE_DEVICES=0
MAX_MEMORY=16GB
ENABLE_MPS=false  # Set to true for MacOS with M1/M2
Update config/models.yaml:

yaml
Copy
llava:
  enabled: true
  model_size: "7b"
  memory_efficient: true
  cache_dir: "models/cache"
  max_length: 512
  temperature: 0.7
4. Running the Integration
bash
Copy
# Start the development server
npm run dev

# In another terminal, start the model server
python scripts/start_model_server.py --model llava
Verification Steps
Open browser to http://localhost:3000
Navigate to Models → LLaVA
Test with sample image:
bash
Copy
curl -X POST http://localhost:3000/api/models/llava/test
Troubleshooting Guide
Common Issues
CUDA Out of Memory
bash
Copy
# Edit config/models.yaml
llava:
  memory_efficient: true
  batch_size: 1
Model Loading Failed
bash
Copy
# Verify model files
python scripts/verify_model_files.py --model llava

# Clear cache
rm -rf models/cache/*
Image Processing Errors
bash
Copy
# Install additional dependencies
pip install Pillow==9.5.0 opencv-python-headless
Memory Management
For systems with limited GPU memory:

yaml
Copy
llava:
  memory_efficient: true
  offload_to_cpu: true
  quantize: true
Performance Optimization
GPU Optimization
bash
Copy
# Enable GPU memory optimization
export CUDA_LAUNCH_BLOCKING=1
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
Batch Processing
python
Copy
# Example batch processing configuration
batch_size: 4
max_batch_tokens: 2048
Health Check
Run the following to verify your setup:

bash
Copy
# Run integration tests
npm run test:integration

# Run model benchmarks
python scripts/benchmark_llava.py

# Check memory usage
nvidia-smi  # For GPU
htop        # For CPU
Monitoring
bash
Copy
# Monitor GPU usage
watch -n 1 nvidia-smi

# Monitor model server
tail -f logs/model_server.log
Updating
bash
Copy
# Update model weights
python scripts/update_llava.py

# Update dependencies
pip install -r requirements.txt --upgrade
npm install
Security Notes
API Rate Limiting:
yaml
Copy
security:
  rate_limit: 100  # requests per minute
  max_tokens: 4096
Image Validation:
yaml
Copy
security:
  max_image_size: 5MB
  allowed_formats: ["jpg", "png", "jpeg"]
Support
For issues:

Check logs: tail -f logs/model_server.log
Run diagnostics: python scripts/diagnose.py
Create issue on GitHub with logs and system info