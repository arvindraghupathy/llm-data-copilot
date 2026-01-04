from typing import Iterable, List
import ollama

from app.domain.analysis.router import is_analytical
from app.domain.analysis.service import answer_question
from app.domain.chat.rewrite_question_prompt import REWRITE_PROMPT
from app.schemas.chat import ChatMessage
from app.domain.retrieval.service import retrieve_context
from app.domain.chat.prompt import build_prompt


def stream_ollama_response(
    *,
    dataset_id: str,
    messages: List[ChatMessage],
    model: str = "llama3.1:8b",
):

    user_question = messages[-1].content
    standalone_question = rewrite_question(
        history=messages[:-1],
        question=user_question,
    )

    if is_analytical(standalone_question):
        result = answer_question(
            dataset_id=dataset_id,
            question=standalone_question,
        )
        if result is not None:
            for event in stream_analysis_explanation(result=result):
                yield event

            # Optionally: analytical citations
            yield {
                "type": "citations",
                "citations": [
                    {"source": "dataset_rows"}
                ],
            }
            return

    # 1️⃣ Retrieve context
    context_chunks = retrieve_context(
        dataset_id=dataset_id,
        query=standalone_question,
    )
    

    # 2️⃣ Build RAG prompt
    rag_messages = build_prompt(
        context_chunks=[c["text"] for c in context_chunks],
        user_question=standalone_question,
    )
    

    citations = [
        {
            "source": c["source"],
            "sheet": c.get("sheet"),
            "row_index": c.get("row_index"),
            "document_id": c.get("document_id"),
            "filename": c.get("filename"),
        }
        for c in context_chunks
    ]

    # 3️⃣ Stream from Ollama
    response = ollama.chat(
        model=model,
        messages=rag_messages,
        stream=True,
    )

    for chunk in response:
        if "message" in chunk and "content" in chunk["message"]:
            yield {
                "type": "token",
                "content": chunk["message"]["content"],
            }

    # 5️⃣ Send citations at the end
    yield {
        "type": "citations",
        "citations": citations,
    }


def rewrite_question(
    *,
    history: List[ChatMessage],
    question: str,
    model: str = "llama3.1:8b",
) -> str:
    if not history:
        return question

    conversation = "\n".join(
        f"{m.role}: {m.content}" for m in history
    )

    prompt = REWRITE_PROMPT.format(
        conversation=conversation,
        question=question,
    )

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You rewrite questions. You never answer them.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    rewritten = response["message"]["content"].strip()

    # Safety: fallback if model misbehaves
    if not rewritten:
        return question

    return rewritten

def stream_analysis_explanation(
    *,
    result: list[dict],
    model: str = "llama3.1:8b",
) -> Iterable[dict]:
    # 1️⃣ Send the structured result FIRST
    yield {
        "type": "result",
        "rows": result,
    }

    # 2️⃣ Build explanation prompt
    prompt = f"""
You are a data assistant.

Using the computed result below, answer the user's question clearly
and concisely.

Computed result (JSON):
{result}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "You explain computed data results."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    # 3️⃣ Stream explanation tokens
    for chunk in response:
        if "message" in chunk and "content" in chunk["message"]:
            yield {
                "type": "token",
                "content": chunk["message"]["content"],
            }

    # 4️⃣ Signal completion
    yield {"type": "done"}