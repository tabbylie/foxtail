from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login.user_loader
	def load_user(id):
		return User.query.get(int(id))

	def __repr__(self):
		return f'<User {self.username}>'

class Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	desc = db.Column(db.String(128), index=True, unique=True)
	price = db.Column(db.Integer, index=True)

	def __repr__(self):
		return f'<Product {self.name}>'

class Orders(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	order_name = db.Column(db.String(64), index=True)
	order_desc = db.Column(db.String(128), index=True, unique=True)
	time_ordered = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	order_flag = db.Column(db.String(32), index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Post {self.order_name}'