
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, func
from app.infra.db.session import Base

class DatasetDocument(Base):
    __tablename__ = "dataset_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_id: Mapped[str] = mapped_column(ForeignKey("datasets.id"))
    filename: Mapped[str]
    content_type: Mapped[str]  # "docx"
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
