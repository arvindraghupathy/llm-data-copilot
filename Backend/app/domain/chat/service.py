from typing import List
from app.schemas.chat import ChatMessage

def answer_question(
    *,
    dataset_id: str,
    messages: List[ChatMessage],
    db,
) -> str:
    # TODO:
    # 1. Retrieve dataset
    # 2. Query vector store using last user message
    # 3. Feed context + history to LLM

    last_user_msg = messages[-1].content

    # Temporary stub
    return f"(Stub) You asked about dataset {dataset_id}: {last_user_msg}"
