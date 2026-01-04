# LLM Excel Copilot

A full-stack application that lets users upload arbitrary Excel datasets
and ask analytical or conversational questions using LLMs.

## Why this project

This project explores how LLMs can act as data copilots over arbitrary,
unknown datasets without predefined schemas or pipelines.

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


## Architecture Overview

- Excel files are ingested into Postgres (JSONB) and Qdrant
- Conversational queries use RAG over vector search
- Analytical queries are translated into safe, read-only SQL
- Responses are streamed to the UI using SSE
- Local LLM inference via Ollama
