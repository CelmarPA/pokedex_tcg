from ..activity.results import ActivitySummary
from ..activity.service import activity_service
from ..models import Activity
from ..cards.service import card_service
from ..statistics.service import statistics_service
from ..achievement.service import achievement_service
from .results import Dashboard


class DashboardService:

    def get_dashboard_data(self, user):

        stats = statistics_service.get_user_statistics(user)

        ach_progress = achievement_service.get_user_achievements_progress(user)

        collection_progress = statistics_service.get_collection_progress(user)[:6]

        favorite_types = statistics_service.get_favorite_types(user)

        collection_rarity = statistics_service.get_collection_rarity(user)

        types_chart = statistics_service.get_types_chart(user)

        rarity_chart = statistics_service.get_rarity_chart(user)

        activities = activity_service.get_recent_summary(user)

        return Dashboard(
            recent_activities=activities,
            stats=stats,
            ach_progress=ach_progress,
            collection_progress=collection_progress,
            favorite_types=favorite_types,
            collection_rarity=collection_rarity,
            type_chart=types_chart,
            rarity_chart=rarity_chart,
        )


dashboard_service = DashboardService()