# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from integrations.codellama_integration import router as codellama_router

app = FastAPI(title="AI Explorer")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(codellama_router)
