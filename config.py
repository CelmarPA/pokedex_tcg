import os
from dotenv import load_dotenv
from secrets import token_hex


load_dotenv()


class Config:

    SECRET_KEY: str = os.environ.get("SECRET_KEY") or token_hex(32)

    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
