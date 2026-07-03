from dataclasses import dataclass
from ..statistics.results import Statistics, ChartData
from ..achievement.results import AchievementsProgress


@dataclass(slots=True)
class Dashboard:

    recent_activities: list
    stats: Statistics
    ach_progress: AchievementsProgress
    collection_progress: list
    favorite_types: list
    collection_rarity: list
    type_chart: ChartData
    rarity_chart: ChartData
