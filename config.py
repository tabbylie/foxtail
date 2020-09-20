import os
from os.path import join, dirname, realpath

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "oO0x6^1aC3%1"

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["officialfoxtail@gmail.com"]

    UPLOAD_FOLDER = os.path.join(basedir, "app/static/profile_imgs/")

    SQLALCHEMY_DATABASE_URI = os.environ.get(DATABASE_URL)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
