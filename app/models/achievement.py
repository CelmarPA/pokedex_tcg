from datetime import datetime, UTC
from sqlalchemy import Integer, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Achievement(db.Model):

    __tablename__ = "achievements"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "achievement_key",
            name="uq_user_achievement"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="achievements")
    achievement_key: Mapped[str] = mapped_column(String(50), nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))