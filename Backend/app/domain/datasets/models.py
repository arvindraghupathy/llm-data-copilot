from dataclasses import dataclass
from datetime import datetime

@dataclass
class Dataset:
    id: str
    filename: str
    created_at: datetime
    row_count: int | None = None
