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

        recent_activities = Activity.query.filter_by(
            user_id=user.id
        ).order_by(
            Activity.created_at.desc()
        ).limit(10).all()

        activities = []

        for activity in recent_activities:
            card = card_service.get_card_smart(activity.card_id)

            activities.append({
                "action": activity.action,
                "card_name": card["name"],
                "created-at": activity.created_at
            })

        type_labels = [item["type"] for item in favorite_types]
        type_values = [item["count"] for item in favorite_types]

        rarity_labels = [item["rarity"] for item in collection_rarity]
        rarity_values = [item["count"] for item in collection_rarity]

        return Dashboard(
            recent_activities=activities,
            stats=stats,
            ach_progress=ach_progress,
            collection_progress=collection_progress,
            favorite_types=favorite_types,
            collection_rarity=collection_rarity,
            type_labels=type_labels,
            type_values=type_values,
            rarity_labels=rarity_labels,
            rarity_values=rarity_values,
        )


dashboard_service = DashboardService()