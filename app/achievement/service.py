from ..extensions import db
from ..models import Achievement, Activity
from ..collection.service import collection_service
from .definitions import ACHIEVEMENTS
from .results import Achievements, AchievementsProgress

class AchievementService:

    def __init__(self):
        self.achievements = ACHIEVEMENTS

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

    def check_collectors(self, user):

        total_cards = sum(card.quantity for card in user.collections)

        if total_cards >= 1:
            self.unlock(user, "FIRST_CARD")

        if total_cards >= 100:
            self.unlock(user, "COLLECTOR_100")

        if total_cards >= 500:
            self.unlock(user, "MASTER_COLLECTOR")

        if total_cards >= 1000:
            self.unlock(user, "LEGENDARY_COLLECTOR")

    def check_favorites(self, user):

        total_favorites = len(user.favorites)

        if total_favorites >= 1:
            self.unlock(user, "FIRST_FAVORITE")

        if total_favorites >= 25:
            self.unlock(user, "FAVORITE_TRAINER")

        if total_favorites >= 100:
            self.unlock(user, "FAVORITE_MASTER")

    def check_wishlist(self, user):

        total_wishlists = len(user.wishlists)

        if total_wishlists >= 1:
            self.unlock(user, "FIRST_WISHLIST")

        if total_wishlists >= 50:
            self.unlock(user, "WISHLIST_BUILDER")

        if total_wishlists >= 150:
            self.unlock(user, "MASTER_WISHLIST")

    def check_sets(self, user):

        progress = collection_service.get_collection_progress(user)

        completed_sets = sum(1 for set_data in progress if set_data.progress == 100)

        if completed_sets >= 1:
            self.unlock(user, "FIRST_SET")

        if completed_sets >= 5:
            self.unlock(user, "SET_COLLECTOR")

        if completed_sets >= 10:
            self.unlock(user, "MASTER_SET_COLLECTOR")

    def check_collection_value(self, user):

        value = collection_service.get_collection_value(user)

        if value >= 500:
            self.unlock(user, "VALUABLE_COLLECTION")

        if value >= 1000:
            self.unlock(user, "MILLIONAIRE")

        if value >= 5000:
            self.unlock(user, "INVESTOR")

    def check_activity(self, user):

        total_activities = Activity.query.filter_by(
            user_id=user.id
        ).count()

        if total_activities >= 100:
            self.unlock(user, "ACTIVE_TRAINER")

        if total_activities >= 500:
            self.unlock(user, "DEDICATED_TRAINER")

    def check_special(self, user):

        total_achievements = len(ACHIEVEMENTS) - 1  # Without POKEDEX_MASTER

        unlocked = len(user.achievements)

        if unlocked == total_achievements:
            self.unlock(user, "POKEDEX_MASTER")

    def check_achievements(self, user):
        self.check_collectors(user)

        self.check_favorites(user)

        self.check_wishlist(user)

        self.check_sets(user)

        self.check_collection_value(user)

        self.check_activity(user)

        self.check_special(user)

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
