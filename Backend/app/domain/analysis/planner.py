
import ollama
from app.domain.analysis.prompt import (
    SQL_PLANNER_SYSTEM_PROMPT,
    SQL_PLANNER_USER_PROMPT,
)

def generate_sql_query(*, question: str, dataset_id: str, schema: dict) -> str:
    prompt = SQL_PLANNER_USER_PROMPT.format(
        question=question,
        schema=schema,
    ).replace("<DATASET_ID>", dataset_id)

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SQL_PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]