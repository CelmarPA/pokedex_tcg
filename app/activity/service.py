from ..models import Activity
from ..extensions import db


class ActivityService:

    def log_activity(self, user_id, card_id, action):

        activity = Activity(
            user_id=user_id,
            card_id=card_id,
            action=action
        )

        db.session.add(activity)


activity_service = ActivityService()
