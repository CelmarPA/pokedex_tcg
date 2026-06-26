from datetime import datetime, UTC
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import db


class CardCache(db.Model):

    __tablename__ = "card_cache"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    data: Mapped[dict] = mapped_column(db.JSON, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(UTC))