# app/models/deckcard.py

from sqlalchemy import Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .deck import Deck


class DeckCard(db.Model):

    __tablename__ = "deck_cards"

    __table_args__ = (UniqueConstraint("deck_id, card_id", name="uq_deck_card"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=False, index=True)
    card_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    deck: Mapped["Deck"] = relationship(back_populates="cards")
