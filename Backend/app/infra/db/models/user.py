from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.infra.db.session import Base

if TYPE_CHECKING:
    from app.infra.db.models.dataset import Dataset

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str | None] = mapped_column(unique=True)
    google_id: Mapped[str | None] = mapped_column(unique=True)

    is_anonymous: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    datasets: Mapped[list["Dataset"]] = relationship(back_populates="user")
