from .results import ActivitySummary
from ..cards.service import card_service
from ..models import Activity
from ..extensions import db


class ActivityService:

    def get_recent(self, user, limit=10):

        return (
            Activity.query
            .filter_by(user_id=user.id)
            .order_by(Activity.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_total(self, user):

        return (
            Activity.query
            .filter_by(user_id=user.id)
            .count()
        )

    def log_activity(self, user_id, card_id, action):

        activity = Activity(
            user_id=user_id,
            card_id=card_id,
            action=action
        )

        db.session.add(activity)

    def get_recent_summary(self, user, limit=10):
        recent = self.get_recent(
            user=user,
            limit=limit
        )

        activities = []

        for activity in recent:

            card = card_service.get_card_smart(activity.card_id)

            activities.append(
                ActivitySummary(
                    action=activity.action,
                    card_name=card["name"],
                    created_at=activity.created_at
                )
            )

        return activities


activity_service = ActivityService()
