# 🤖 Phi-2 Integration Setup Guide
> For AI Explorer Interface Integration

## 📋 Prerequisites
### Required Dependencies
```bash
# Core dependencies
pip install torch>=2.0.0
pip install transformers>=4.36.0
pip install numpy>=1.24.0


1. Repository Set-up
# Clone the repository
git clone https://github.com/your-username/omega-awesome-a2a.git
cd omega-awesome-a2a

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows


2. Model Set-up
# First-time model download and cache
from transformers import AutoModelForCausalLM, AutoTokenizer

# This will trigger the model download
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2")


Configuration
Environment Variables
in bash
# Optional: Set custom cache directory
export HF_HOME="/path/to/cache"  # Linux/Mac
# or
set HF_HOME=C:\path\to\cache  # Windows
🔍 Verification Steps
Test imports:
    python
import torch  # type: ignore
import transformers  # type: ignore
from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
Verify GPU (if available):
with python 
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
🚨 Common Issues & Solutions
CUDA Issues
in bash
# If CUDA not detected, install specific torch version
pip install torch --index-url https://download.pytorch.org/whl/cu118
Memory Issues
Reduce batch size
Use model in half precision:
with python
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype=torch.float16
)
📝 Additional Notes
First run will download ~2.7GB of model files
Cache location: ~/.cache/huggingface/ (default)
Model files are stored locally after first download
🔄 Updates & Maintenance
in bash
# Keep dependencies updated
pip install --upgrade torch transformers

# Clear cache if needed
rm -rf ~/.cache/huggingface/microsoft/phi-2
🏗️ Project Structure
ai-explorer/
├── models/
│   └── phi2/
│       ├── interface.py
│       └── config.json
├── setup.md
└── requirements.txt