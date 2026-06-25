from ..models import Activity
from ..extensions import db


def log_activity(user_id, card_id, action):

    activity = Activity(
        user_id=user_id,
        card_id=card_id,
        action=action
    )

    db.session.add(activity)
