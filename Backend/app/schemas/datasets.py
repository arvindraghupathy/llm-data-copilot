from datetime import datetime
from pydantic import BaseModel
from pydantic.config import ConfigDict

class DatasetInfo(BaseModel):
    dataset_id: str
    filename: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
