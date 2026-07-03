from ..activity.service import activity_service
from ..extensions import db
from ..models import Achievement
from ..collection.service import collection_service
from .definitions import (
    ACHIEVEMENTS,
    COLLECTOR_RULES,
    FAVORITE_RULES,
    WISHLIST_RULES,
    SET_RULES,
    VALUE_RULES,
    ACTIVITY_RULES
)
from .results import Achievements, AchievementsProgress


class AchievementService:
  
    def has_achievement(self, user, achievement_key):

        return Achievement.query.filter_by(
            user_id=user.id,
            achievement_key=achievement_key
        ).first() is not None

    def unlock(self, user, achievement_key):

        if self.has_achievement(user, achievement_key):
            return False

        achievement = Achievement(
            user_id=user.id,
            achievement_key=achievement_key
        )

        db.session.add(achievement)

        return True

    def _unlock_if(self, user, value, required, achievement_key):

        if value >= required:
            self.unlock(user, achievement_key)

    def _process_rules(self, user, value, rules):

        for rule in rules:

            self._unlock_if(
                user=user,
                value=value,
                required=rule.required,
                achievement_key=rule.key
            )

    def _check_collectors(self, user):

        total_cards = collection_service.get_total_cards(user)

        self._process_rules(
            user=user,
            value=total_cards,
            rules=COLLECTOR_RULES
        )

    def _check_favorites(self, user):

        self._process_rules(
            user=user,
            value=len(user.favorites),
            rules=FAVORITE_RULES
        )

    def _check_wishlist(self, user):

        self._process_rules(
            user=user,
            value=len(user.wishlists),
            rules=WISHLIST_RULES
        )

    def _check_sets(self, user):

        progress = collection_service.get_collection_progress(user)

        completed_sets = sum(
            1
            for set_data in progress
            if set_data.progress == 100
        )

        self._process_rules(
            user=user,
            value=completed_sets,
            rules=SET_RULES
        )

    def _check_collection_value(self, user):

        value = collection_service.get_collection_value(user)

        self._process_rules(
            user=user,
            value=value,
            rules=VALUE_RULES
        )

    def _check_activity(self, user):

        total = activity_service.get_total(user)

        self._process_rules(
            user=user,
            value=total,
            rules=ACTIVITY_RULES
        )

    def _check_special(self, user):

        total_achievements = len(ACHIEVEMENTS) - 1  # Without POKEDEX_MASTER

        unlocked = len(user.achievements)

        if unlocked == total_achievements:
            self.unlock(user, "POKEDEX_MASTER")

    def check_achievements(self, user):
        self._check_collectors(user)

        self._check_favorites(user)

        self._check_wishlist(user)

        self._check_sets(user)

        self._check_collection_value(user)

        self._check_activity(user)

        self._check_special(user)

    def get_user_achievements(self, user):

        self.check_achievements(user)

        achievements = []

        unlocked = {
            achievement.achievement_key: achievement for achievement in user.achievements
        }

        for key, data in ACHIEVEMENTS.items():
            achievement = unlocked.get(key)

            achievements.append(Achievements(
                key=key,
                title=data["title"],
                description=data["description"],
                icon=data["icon"],
                unlocked=achievement is not None,
                unlocked_at=achievement.unlocked_at if achievement else None
            ))

        achievements.sort(
            key=lambda item: (
                not item.unlocked,
                item.title
            )
        )

        return achievements

    def get_user_achievements_progress(self, user):

        achievements = self.get_user_achievements(user)

        unlocked = sum(achievement_.unlocked for achievement_ in achievements)

        total = len(achievements)

        progress = (unlocked / total * 100) if total else 0

        return AchievementsProgress(
            achievements=achievements,
            unlocked=unlocked,
            total=total,
            progress=progress
        )


achievement_service = AchievementService()
