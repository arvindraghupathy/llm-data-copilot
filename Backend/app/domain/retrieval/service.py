from typing import List
import structlog
from app.core.config import settings
from app.domain.embeddings.service import embed_text
from app.infra.vector_store.qdrant import QdrantStore
from app.schemas.retrieved_chunck import RetrievedChunk

log = structlog.get_logger()
def retrieve_context(
    *,
    dataset_id: str,
    query: str,
    top_k: int = 5,
) -> List[RetrievedChunk]:
    """
    Returns top-k relevant text chunks for a dataset.
    """
    query_embedding = embed_text(query)

    results = QdrantStore(
        url=settings.qdrant_url,
        collection=settings.qdrant_collection
    ).query(
        vector=query_embedding,
        filters={"dataset_id": dataset_id},
        limit=top_k,
    )

    return [
    RetrievedChunk(
        text=point.payload["text"] if point.payload else "",
        source=point.payload["source"] if point.payload and "source" in point.payload else "excel",
        sheet=point.payload.get("sheet") if point.payload and "sheet" in point.payload else None,
        row_index=point.payload.get("row_index") if point.payload and "row_index" in point.payload else None,
        document_id=point.payload.get("document_id") if point.payload and "document_id" in point.payload else None,
        filename=point.payload.get("filename") if point.payload and "filename" in point.payload else None,
    )
    for point in results
]
