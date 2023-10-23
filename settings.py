import os
import string

ALLOWED_CHARACTERS = string.ascii_letters + string.digits
AUTO_SHORT_ID_LENGTH = 6
PATTERN = r'^[A-Za-z0-9]*$'
SHORT_USER_LENGTH = 16
MAX_ATTEMPTS_CREATE_AUTO_SHORT_ID = 20


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
