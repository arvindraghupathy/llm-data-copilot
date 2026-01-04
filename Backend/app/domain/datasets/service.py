from datetime import datetime
from typing import cast
import uuid
from pathlib import Path
from fastapi import HTTPException
from sqlalchemy.orm import Session
import structlog

from app.core.config import settings
from app.core.status_stream import publish_dataset_status
from app.domain.datasets.ingestion import ingest_excel
from app.infra.db.models.dataset import Dataset, DatasetStatus
from app.infra.db.models.dataset_documents import DatasetDocument
from app.infra.db.models.dataset_rows import DatasetRow
from app.infra.db.session import SessionLocal
from app.infra.vector_store.qdrant import QdrantStore
from app.schemas.datasets import DatasetInfo

log = structlog.get_logger()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def create_dataset(*, file, db: Session) -> str:
    dataset_id = str(uuid.uuid4())
    dataset = Dataset(
        id=dataset_id,
        filename=file.filename,
        status=DatasetStatus.uploaded,
    )

    db.add(dataset)
    db.commit()
    file_path = UPLOAD_DIR / f"{dataset_id}_{file.filename}"

    # Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    log.info("dataset_file_saved", dataset_id=dataset_id)
    return dataset_id



def ingest_dataset_job(dataset_id: str):
    db = SessionLocal()
    vector_store = QdrantStore(
        url=settings.qdrant_url,
        collection=settings.qdrant_collection,
    )

    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            log.error("dataset_not_found", dataset_id=dataset_id)
            return

        dataset.status = DatasetStatus.ingesting
        db.commit()
        publish_dataset_status(dataset_id, "ingesting")

        ingest_excel(
            path=UPLOAD_DIR / f"{dataset_id}_{dataset.filename}",
            dataset_id=dataset_id,
            vector_store=vector_store,
        )

        dataset.status = DatasetStatus.ready
        db.commit()
        publish_dataset_status(dataset_id, "ready")
        log.info("dataset_ingested", dataset_id=dataset_id)

    except Exception as e:
        log.error("Error ingesting dataset", error=e)
        log.exception("dataset_ingestion_failed", dataset_id=dataset_id)
        if dataset:
            dataset.status = DatasetStatus.failed
            db.commit()
            publish_dataset_status(dataset_id, "failed")

    finally:
        db.close()



def delete_dataset(
    *,
    dataset_id: str,
    db: Session,
    vector_store,
):
    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # 1️⃣ Delete vectors first (safe to retry)
    vector_store.delete_dataset(dataset_id)

    # 2️⃣ Delete DB row
    db.delete(dataset)
    db.query(DatasetRow).filter(DatasetRow.dataset_id == dataset_id).delete()
    db.query(DatasetDocument).filter(DatasetDocument.dataset_id == dataset_id).delete()
    db.commit()


def get_dataset(
    *,
    dataset_id: str,
    db: Session,
):
    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    

    return DatasetInfo(
        dataset_id=dataset.id,
        filename=dataset.filename,
        status=dataset.status.value if hasattr(dataset.status, "value") else str(dataset.status),
        created_at=cast(datetime, dataset.created_at),
    )

def list_rows(
    *,
    dataset_id: str,
    db: Session,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    rows = (
        db.query(DatasetRow)
        .filter(DatasetRow.dataset_id == dataset_id)
        .order_by(DatasetRow.row_index)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total = (
        db.query(DatasetRow)
        .filter(DatasetRow.dataset_id == dataset_id)
        .count()
    )

    return {
        "rows": [r.data for r in rows],
        "total": total,
    }