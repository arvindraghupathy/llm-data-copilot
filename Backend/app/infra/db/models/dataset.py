from sqlalchemy import (
    DateTime,
    ForeignKey,
    Enum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.infra.db.session import Base
from app.infra.db.models.user import User

class DatasetStatus(enum.Enum):
    uploaded = "uploaded"
    ingesting = "ingesting"
    ready = "ready"
    failed = "failed"

class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    filename: Mapped[str]
    status: Mapped[DatasetStatus] = mapped_column(
        Enum(DatasetStatus),
        default=DatasetStatus.uploaded,
    )

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship(User, back_populates="datasets")
