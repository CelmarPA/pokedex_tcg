from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class Achievements:

    key: str
    title: str
    description: str
    icon: str
    unlocked: bool
    unlocked_at: datetime | None


@dataclass(slots=True)
class AchievementsProgress:

    achievements: list
    unlocked: int
    total: int
    progress: float = 0
