import uuid
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Iterator, cast
from datetime import datetime, date

from app.domain.embeddings.service import embed_text
from app.infra.db.models.dataset_rows import DatasetRow
from app.infra.db.session import SessionLocal
from app.infra.vector_store.qdrant import QdrantStore


def to_json_safe(value):
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    return value


def ingest_excel(*, path: Path, dataset_id: str, vector_store: QdrantStore) -> bool:
    """
    Yields normalized text chunks with metadata and stores rows for UI.
    """
    xls = pd.ExcelFile(path)
    db = SessionLocal()

    try:
        for sheet_name in xls.sheet_names:
            df = cast(pd.DataFrame, xls.parse(sheet_name))

            df.columns = pd.Index([str(c).strip() for c in df.columns])

            for i, (_, row) in enumerate(df.iterrows()):
                row_dict = {
                    col: to_json_safe(val)
                    for col, val in row.items()
                }

                db.add(
                    DatasetRow(
                        dataset_id=dataset_id,
                        row_index=int(i),
                        data=row_dict,
                    )
                )

                # Build RAG text
                text_parts = [
                    f"{col}: {row_dict[col]}"
                    for col in row_dict
                    if row_dict[col] is not None
                ]

                chunk = {
                    "text": "\n".join(text_parts),
                    "metadata": {
                        "sheet": sheet_name,
                        "row_index": int(i),
                    },
                }

                embedding = embed_text(chunk["text"])

                vector_store.upsert(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "dataset_id": dataset_id,
                        "source": "excel",
                        "sheet": sheet_name,
                        "row_index": int(i),
                        **chunk["metadata"],
                        "text": chunk["text"],
                    },
                )

        db.commit()
        return True
    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
