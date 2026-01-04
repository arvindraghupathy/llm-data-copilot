from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.infra.db.session import Base
from sqlalchemy import ForeignKey

class DatasetRow(Base):
    __tablename__ = "dataset_rows"

    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_id: Mapped[str] = mapped_column(ForeignKey("datasets.id"))
    row_index: Mapped[int]
    data: Mapped[dict] = mapped_column(JSONB)  # JSON column
