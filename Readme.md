# LLM Excel Copilot

A full-stack application that lets users upload arbitrary Excel datasets
and ask analytical or conversational questions using LLMs.

## Features
- Upload Excel files
- Automatic ingestion into Postgres (JSONB)
- Conversational chat (RAG + SQL analysis)
- Safe LLM-generated SQL execution
- Streaming responses (SSE)
- Dataset-agnostic (works with any Excel)

## Tech Stack
- Backend: FastAPI, SQLAlchemy, Postgres
- Frontend: Next.js, React, Tailwind
- LLM: Ollama (local)
- Vector DB: Qdrant
- Streaming: Server-Sent Events

## Getting Started

### Prerequisites
- Docker
- Node.js
- Python 3.11+
- Ollama running locally

### Run Backend
```bash
cd backend
cp .env.example .env
poetry install
poetry run uvicorn app.main:app --reload
