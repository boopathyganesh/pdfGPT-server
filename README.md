# AI Document Q&A App - Backend

This is the backend for the Document Q&A application, built with **FastAPI**. It handles PDF uploads, chunking, document processing, and real-time AI Q&A using WebSockets and Perplexity AI.

## Features

- Accept multiple PDF uploads
- Extract and chunk content using PyMuPDF
- Vector-based context matching (basic in-memory or custom logic, no pgvector)
- WebSocket endpoint for chat interaction
- Uses Perplexity AI for final answer generation

## Technologies

- FastAPI
- PyMuPDF (fitz)
- WebSocket support via FastAPI
- Perplexity API
- CORS middleware
## Setup Instructions

```bash

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Run Locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
## Endpoints
- POST /upload
-- Accepts multiple PDF files and extracts content into memory.

- POST /ask
-- Accepts a question and returns AI-generated answer based on uploaded docs.

- GET /ws/chat
-- WebSocket endpoint for real-time Q&A.

## Environment Variables
- PERPLEXITY_API_KEY=your_api_key_here