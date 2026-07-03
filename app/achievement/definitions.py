from .rules import AchievementRule


ACHIEVEMENTS = {

    # =========================
    # COLLECTION
    # =========================

    "FIRST_CARD": {
        "title": "First Card",
        "description": "Add your first card.",
        "icon": "🎴"
    },

    "COLLECTION_100": {
        "title": "Collector",
        "description": "Own 100 cards.",
        "icon": "📚"
    },

    "MASTER_COLLECTOR": {
        "title": "Master Collector",
        "description": "Own 500 cards.",
        "icon": "🏆",
    },

    "LEGENDARY_COLLECTOR": {
        "title": "Legendary Collector",
        "description": "Own 1000 cards.",
        "icon": "👑",
    },

    # =========================
    # FAVORITES
    # =========================

    "FIRST_FAVORITE": {
        "title": "First Favorite",
        "description": "Add your first favorite card.",
        "icon": "⭐",
    },

    "FAVORITE_TRAINER": {
        "title": "Favorite Trainer",
        "description": "Add 25 favorite cards.",
        "icon": "❤️",
    },

    "FAVORITE_MASTER": {
        "title": "Favorite Master",
        "description": "Add 100 favorite cards.",
        "icon": "🌟",
    },

    # =========================
    # WISHLIST
    # =========================

    "FIRST_WISHLIST": {
        "title": "Dream Begins",
        "description": "Add your first card to the wishlist.",
        "icon": "🎯",
    },

    "WISHLIST_BUILDER": {
        "title": "Wishlist Builder",
        "description": "Add 50 cards to your wishlist.",
        "icon": "📝",
    },

    "MASTER_WISHLIST": {
        "title": "Master Wishlist",
        "description": "Add 150 cards to your wishlist.",
        "icon": "📌",
    },

    # =========================
    # SETS
    # =========================

    "FIRST_SET": {
        "title": "Set Starter",
        "description": "Complete your first Pokémon TCG set.",
        "icon": "📦",
    },

    "SET_COLLECTOR": {
        "title": "Set Collector",
        "description": "Complete 5 Pokémon TCG sets.",
        "icon": "🧩",
    },

    "MASTER_SET_COLLECTOR": {
        "title": "Master Set Collector",
        "description": "Complete 10 Pokémon TCG sets.",
        "icon": "💎",
    },

    # =========================
    # COLLECTION VALUE
    # =========================

    "VALUABLE_COLLECTION": {
        "title": "Valuable Collection",
        "description": "Reach a collection value of $500.",
        "icon": "💵",
    },

    "MILLIONAIRE": {
        "title": "Millionaire",
        "description": "Reach a collection value of $1,000.",
        "icon": "💰",
    },

    "INVESTOR": {
        "title": "Investor",
        "description": "Reach a collection value of $5,000.",
        "icon": "🏦",
    },

    # =========================
    # ACTIVITY
    # =========================

    "ACTIVE_TRAINER": {
        "title": "Active Trainer",
        "description": "Perform 100 collection activities.",
        "icon": "⚡",
    },

    "DEDICATED_TRAINER": {
        "title": "Dedicated Trainer",
        "description": "Perform 500 collection activities.",
        "icon": "🔥",
    },

    # =========================
    # SPECIAL
    # =========================

    "POKEDEX_MASTER": {
        "title": "Pokédex Master",
        "description": "Unlock every available achievement.",
        "icon": "👑",
    },

}


COLLECTOR_RULES = (
    AchievementRule(1, "FIRST_CARD"),
    AchievementRule(100, "COLLECTOR_100"),
    AchievementRule(500, "MASTER_COLLECTOR"),
    AchievementRule(1000, "LEGENDARY_COLLECTOR"),
)


FAVORITE_RULES = (
    AchievementRule(1, "FIRST_FAVORITE"),
    AchievementRule(25, "FAVORITE_TRAINER"),
    AchievementRule(100, "FAVORITE_MASTER")
)


WISHLIST_RULES = (
    AchievementRule(1, "FIRST_WISHLIST"),
    AchievementRule(50, "WISHLIST_BUILDER"),
    AchievementRule(150, "MASTER_WISHLIST")
)


SET_RULES = (
    AchievementRule(1, "FIRST_SET"),
    AchievementRule(5, "SET_COLLECTOR"),
    AchievementRule(10, "MASTER_SET_COLLECTOR")
)


VALUE_RULES = (
    AchievementRule(500, "VALUABLE_COLLECTION"),
    AchievementRule(1000, "MILLIONAIRE"),
    AchievementRule(5000, "INVESTOR")
)


ACTIVITY_RULES = (
    AchievementRule(100, "ACTIVE_TRAINER"),
    AchievementRule(500, "DEDICATED_TRAINER")
)
