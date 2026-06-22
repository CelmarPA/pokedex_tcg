# app/__init__.py
from flask import Flask
from .extensions import db, migrate, login_manager
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

    return app
