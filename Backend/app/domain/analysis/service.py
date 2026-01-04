from sqlalchemy.orm import Session
import structlog
from app.domain.analysis.schema import infer_schema
from app.domain.analysis.planner import generate_sql_query
from app.domain.analysis.executor import execute_sql
from app.domain.analysis.router import is_analytical
from app.infra.db.models.dataset_rows import DatasetRow
from app.infra.db.session import SessionLocal

def answer_question(
    *,
    dataset_id: str,
    question: str,
    db: Session = SessionLocal(),
):
    if not is_analytical(question):
        return None  # fall back to RAG

    rows = (
        db.query(DatasetRow)
        .filter(DatasetRow.dataset_id == dataset_id)
        .all()
    )

    row_dicts = [r.data for r in rows]

    schema = infer_schema(row_dicts)
    query = generate_sql_query(question=question, dataset_id=dataset_id, schema=schema)
    
   
    if not query:
        return None  # fallback to RAG

    rows = execute_sql(sql=query, db=db)
    
    return rows
