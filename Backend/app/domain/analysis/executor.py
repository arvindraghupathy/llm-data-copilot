import re

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import structlog

from app.infra.db.session import SessionLocal

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke)\b",
    re.IGNORECASE,
)

def normalize_sql(sql: str) -> str:
    sql = sql.strip()

    # Remove markdown fences
    if sql.startswith("```"):
        sql = re.sub(r"^```[a-zA-Z]*", "", sql)
        sql = sql.replace("```", "")

    # Remove trailing semicolon
    sql = sql.rstrip().rstrip(";")

    return sql.strip()

def is_safe_sql(sql: str) -> bool:
    sql_l = sql.lower()

    # Must be SELECT (allow WITH … SELECT)
    if not (sql_l.startswith("select") or sql_l.startswith("with")):
        return False

    # Must not contain forbidden statements
    if FORBIDDEN.search(sql):
        return False

    # No multiple statements
    if ";" in sql:
        return False

    return True


def execute_sql(
    *,
    sql: str,
    db: Session = SessionLocal(), 
):
    sql = normalize_sql(sql)
    if not is_safe_sql(sql):
        return []
    
    result = db.execute(text(sql))
    return [dict(row) for row in result.mappings().all()]