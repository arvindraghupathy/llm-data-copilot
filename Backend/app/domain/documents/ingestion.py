from uuid import uuid4
from pathlib import Path

from app.domain.documents.docx_reader import extract_docx_text
from app.domain.documents.chunking import chunk_text
from app.domain.embeddings.service import embed_text
from app.infra.vector_store.qdrant import QdrantStore


def ingest_docx(
    *,
    path: Path,
    dataset_id: str,
    vector_store: QdrantStore,
    doc_id: int,
):
    text = extract_docx_text(str(path))
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)

        vector_store.upsert(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "dataset_id": dataset_id,
                "source": "docx",
                "filename": path.name,
                "doc_id": doc_id,
                "chunk_index": i,
                "text": chunk,
            },
        )
