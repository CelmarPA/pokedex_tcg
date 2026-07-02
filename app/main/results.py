from dataclasses import dataclass
from ..statistics.results import Statistics
from ..achievement.results import AchievementsProgress


@dataclass(slots=True)
class Dashboard:

    recent_activities: list
    stats: Statistics
    ach_progress: AchievementsProgress
    collection_progress: list
    favorite_types: list
    collection_rarity: list
    type_labels: list
    type_values: list
    rarity_labels: list
    rarity_values: list
