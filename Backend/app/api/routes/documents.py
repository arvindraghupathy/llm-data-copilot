from fastapi import APIRouter, Depends, UploadFile, File
from pathlib import Path
import tempfile

from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.documents.ingestion import ingest_docx
from app.infra.db.deps import get_db
from app.infra.db.models.dataset_documents import DatasetDocument
from app.infra.db.session import SessionLocal
from app.infra.vector_store.qdrant import QdrantStore

router = APIRouter()

def get_vector_store():
    return QdrantStore(
        url=settings.qdrant_url,
        collection=settings.qdrant_collection,
    )



@router.post("/{dataset_id}/documents/upload")
async def upload_document_api(
    dataset_id: str,
    vector_store: QdrantStore = Depends(get_vector_store),
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.endswith(".docx"):
        return {"error": "Only DOCX supported"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    
    db = SessionLocal()
    try:
        doc = DatasetDocument(
            dataset_id=dataset_id,
            filename=file.filename,
            content_type="docx",
        )
        db.add(doc)
        db.commit()
        new_doc_id = doc.id
    finally:
        db.close()

    ingest_docx(
        path=tmp_path,
        dataset_id=dataset_id,
        vector_store=vector_store,
        doc_id=new_doc_id,
    )
    return {"status": "uploaded"}


@router.get("/{dataset_id}/documents")
def list_documents_api(
    dataset_id: str,
    db: Session = Depends(get_db),
):
    docs = (
        db.query(DatasetDocument)
        .filter(DatasetDocument.dataset_id == dataset_id)
        .order_by(DatasetDocument.created_at.desc())
        .all()
    )

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "content_type": d.content_type,
            "created_at": d.created_at,
        }
        for d in docs
    ]