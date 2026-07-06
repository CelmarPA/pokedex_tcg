# app/models/deck.py

from datetime import datetime, UTC
from sqlalchemy import Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User
    from .deckcard import DeckCard


class Deck(db.Model):

    __tablename__ = "decks"

    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_deck_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    user: Mapped["User"] = relationship(back_populates="decks")
    cards: Mapped[list["DeckCard"]] = relationship(back_populates="deck", cascade="all, delete-orphan")
