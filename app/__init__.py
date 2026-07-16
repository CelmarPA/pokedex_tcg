# app/__init__.py
from flask import Flask
from .extensions import db, migrate, login_manager, csrf
from config import Config
from .models import User


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app(config_class=Config) -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)    # Link the extension to the app only now
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .cards import cards as cards_blueprint
    app.register_blueprint(cards_blueprint, url_prefix="/cards")

    from .collection import collection as collection_blueprint
    app.register_blueprint(collection_blueprint, url_prefix="/collection")

    from .favorite import favorite as favorite_blueprint
    app.register_blueprint(favorite_blueprint, url_prefix="/favorite")

    from .wishlist import wishlist as wishlist_blueprint
    app.register_blueprint(wishlist_blueprint, url_prefix="/wishlist")

    from .statistics import statistics as statistics_blueprint
    app.register_blueprint(statistics_blueprint, url_prefix="/statistics")

    from .progress import progress as progress_blueprint
    app.register_blueprint(progress_blueprint, url_prefix="/progress")

    from .activity import activity as activity_blueprint
    app.register_blueprint(activity_blueprint, url_prefi="/activity")

    from .achievement import achievement as achievement_blueprint
    app.register_blueprint(achievement_blueprint, url_prefix="/achievement")

    from .deck import deck as deck_blueprint
    app.register_blueprint(deck_blueprint, url_prefix="/deck")

    return app
