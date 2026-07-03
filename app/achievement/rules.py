from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AchievementRule:

    required: int
    key: str
