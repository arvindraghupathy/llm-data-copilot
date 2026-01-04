from typing import TypedDict, Optional

class RetrievedChunk(TypedDict):
    text: str
    source: str
    sheet: Optional[str]
    row_index: Optional[int]
    document_id: Optional[str]
    filename: Optional[str]
