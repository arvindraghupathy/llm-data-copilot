from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.core.tracing import setup_tracing
from app.api.routes import documents, health
from app.api.routes import datasets, chat

def create_app():
    setup_logging()
    setup_tracing()

    app = FastAPI(title="RAG Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
    app.include_router(chat.router, prefix="/datasets", tags=["chat"])
    app.include_router(documents.router, prefix="/datasets", tags=["documents"])
    return app

app = create_app()

