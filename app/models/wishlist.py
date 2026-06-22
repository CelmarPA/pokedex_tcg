from datetime import datetime, UTC
from sqlalchemy import Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User


class Wishlist(db.Model):

    __tablename__ = "wishlists"

    __table_args__ = (UniqueConstraint("user_id", "card_id", name="uq_user_card_wishlist"),)

    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="wishlists")
    card_id: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
