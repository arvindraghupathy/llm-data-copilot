from datetime import datetime
import json
from typing import cast
from fastapi import APIRouter, UploadFile, BackgroundTasks, File, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.status_stream import subscribe_dataset, subscribe_global
from app.infra.db.deps import get_db
from app.infra.db.models.dataset import Dataset
from app.schemas.datasets import DatasetInfo
from app.infra.vector_store.qdrant import QdrantStore
from app.domain.datasets.service import create_dataset, delete_dataset, get_dataset, ingest_dataset_job, list_rows
from app.core.config import settings

router = APIRouter()

def get_vector_store():
    return QdrantStore(
        url=settings.qdrant_url,
        collection=settings.qdrant_collection,
    )

@router.post("/upload", response_model=DatasetInfo)
def upload_dataset(
    file: UploadFile = File(...),
    
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    dataset_id = create_dataset(file=file, db=db)
    background_tasks.add_task(ingest_dataset_job, dataset_id=dataset_id)
    return DatasetInfo(
        dataset_id=dataset_id,
        filename=file.filename or "",
        status="uploaded",
        created_at=datetime.now(),
    )

@router.get("/list", response_model=list[DatasetInfo])
def list_datasets(
    db: Session = Depends(get_db),
):
    datasets = (
        db.query(Dataset)
        .order_by(Dataset.created_at.desc())
        .all()
    )
    return [
        DatasetInfo(
            dataset_id=d.id,
            filename=d.filename,
            status=d.status.value if hasattr(d.status, "value") else str(d.status),
            created_at=cast(datetime, d.created_at),
        )
        for d in datasets
    ]

@router.delete("/{dataset_id}", status_code=204)
def delete_dataset_api(
    dataset_id: str,
    vector_store: QdrantStore = Depends(get_vector_store),
    db: Session = Depends(get_db),
):
    delete_dataset(
        dataset_id=dataset_id,
        db=db,
        vector_store=vector_store,
    )

@router.get("/{dataset_id}")
def get_dataset_api(
    dataset_id: str,
    db: Session = Depends(get_db),
):
    return get_dataset(
        dataset_id=dataset_id,
        db=db,
    )

@router.get("/{dataset_id}/rows")
def list_rows_api(
    dataset_id: str,
    page: int = 1,
    page_size: int = 25,
    db: Session = Depends(get_db),
):
    return list_rows(
        dataset_id=dataset_id,
        page=page,
        page_size=page_size,
        db=db,
    )



@router.get("/{dataset_id}/status/stream")
async def stream_dataset_status(dataset_id: str):
    queue = subscribe_dataset(dataset_id)

    async def event_generator():
        while True:
            status = await queue.get()
            yield f"data: {json.dumps(status)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


@router.get("/status/stream")
async def stream_all_dataset_status():
    queue = subscribe_global()

    async def event_generator():
        while True:
            event = await queue.get()
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
