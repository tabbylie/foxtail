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

    SQLALCHEMY_DATABASE_URI = "postgres://wgxpnadimafppk:1b6656695ebcf832417c2bdcab0929b3cc9d93c1a4af02afe3a3219cbaca53bd@ec2-50-19-26-235.compute-1.amazonaws.com:5432/ddmqpqnpbdklb6"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # "postgres://wgxpnadimafppk:1b6656695ebcf832417c2bdcab0929b3cc9d93c1a4af02afe3a3219cbaca53bd@ec2-50-19-26-235.compute-1.amazonaws.com:5432/ddmqpqnpbdklb6"
    # "sqlite:///" + os.path.join(basedir, "tail.db")