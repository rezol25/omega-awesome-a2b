Install Dependencies
bash
Copy
npm install

Environment Setup
bash
Copy
cp .env.example .env

Add the following to your .env:

env
Copy
MISTRAL_API_KEY=your_api_key
MISTRAL_ENDPOINT=your_endpoint
RAG_VECTOR_STORE_PATH=./vector_store

Model Setup
bash
Copy
npm run setup:mistral

Verification
bash
Copy
npm run test:mistral

Usage
Start the application:
bash
Copy
npm run dev

Navigate to http://localhost:3000
Select "Mistral-7B RAG" from the model dropdown
Begin using the interface
Troubleshooting
Issue: CUDA out of memory Solution: Reduce batch size in config
Issue: Vector store initialization failed Solution: Check file permissions