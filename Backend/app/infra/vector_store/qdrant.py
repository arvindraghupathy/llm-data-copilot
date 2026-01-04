from qdrant_client import QdrantClient
from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, VectorParams, PointStruct
from .base import VectorStore
from app.core.config import settings

class QdrantStore(VectorStore):
    def __init__(self, url: str, collection: str, vector_size: int | None = None):
        self.client = QdrantClient(url=url)
        self.collection = collection
        self.vector_size = vector_size if vector_size is not None else settings.embedding_dim
        self._ensure_collection()

    def upsert(self, *, id, vector, payload):
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def query(self, *, vector, filters, limit):
        # Build Qdrant filter from simple dict of equals conditions
        qdrant_filter = None
        if filters:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value),
                    )
                    for key, value in filters.items()
                ]
            )

        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
            query_filter=qdrant_filter,
        )

        # Return top-k texts from payloads
        return response.points

    def _ensure_collection(self):
        # Create collection if it does not exist
        try:
            collections = self.client.get_collections()
            names = {c.name for c in getattr(collections, "collections", [])}
            if self.collection not in names:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE,
                    ),
                )
            else:
                # Validate vector size; recreate if mismatched
                info = self.client.get_collection(collection_name=self.collection)
                vectors_cfg = getattr(getattr(info, "config", None), "params", None)
                vectors_cfg = getattr(vectors_cfg, "vectors", None)
                current_size = None
                if isinstance(vectors_cfg, VectorParams):
                    current_size = vectors_cfg.size
                elif isinstance(vectors_cfg, dict) and vectors_cfg:
                    any_params = next(iter(vectors_cfg.values()))
                    if isinstance(any_params, VectorParams):
                        current_size = any_params.size
                if current_size is not None and current_size != self.vector_size:
                    self.client.delete_collection(collection_name=self.collection)
                    self.client.create_collection(
                        collection_name=self.collection,
                        vectors_config=VectorParams(
                            size=self.vector_size,
                            distance=Distance.COSINE,
                        ),
                    )
        except Exception:
            # Best-effort create in case listing failed
            try:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE,
                    ),
                )
            except Exception:
                # If it still fails (e.g., already exists or connection issue), let upstream handle
                pass
    
    def delete_dataset(self, dataset_id: str):
        self.client.delete(
            collection_name=self.collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="dataset_id",
                        match=MatchValue(value=dataset_id),
                    )
                ]
            ),
        )
