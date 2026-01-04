import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import traceback

from app.schemas.chat import ChatRequest
from app.domain.chat.ollama_service import stream_ollama_response
from app.infra.db.deps import get_db

router = APIRouter()


@router.post("/{dataset_id}/chat")
def chat_stream(
    dataset_id: str,
    body: ChatRequest,
    db: Session = Depends(get_db),
):
    def event_generator():
        try:
            for token in stream_ollama_response(
                dataset_id=dataset_id,
                messages=body.messages,
            ):

                # IMPORTANT: must flush valid SSE frames
                yield f"data: {json.dumps(token)}\n\n"

        except Exception as e:
            # Send error as SSE frame (prevents abrupt close)
            yield f"data: [ERROR] {str(e)}\n\n"
            traceback.print_exc()

        finally:
            # ALWAYS send DONE
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
