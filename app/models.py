from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from time import time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile_img = db.Column(db.String(128))
    orders = db.relationship("Orders", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset password": self.id, "exp": time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        try:
            ids = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                "reset password"
            ]
        except:
            return
        return User.query.get(ids)

    def __repr__(self):
        return f"<User {self.username}>"


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    desc = db.Column(db.String(256), index=True, unique=True)
    price = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f"<Product {self.name}>"


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(64), index=True)
    order_desc = db.Column(db.String(128), index=True)
    time_ordered = db.Column(
        db.String(32),
        index=True,
        default=datetime.utcnow().strftime("%b, %a %d, %Y %I:%M%p"),
    )
    order_flag = db.Column(db.String(32), index=True, default="open")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Order {self.order_name}>"
