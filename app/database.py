from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from datetime import datetime



sql = SQLAlchemy()

class WechatUser(sql.Model, UserMixin):
	__tablename__ = 'wechatuser'
	id = sql.Column(sql.Integer, primary_key = True, autoincrement = True)
	username = sql.Column(sql.String(50), nullable = False)
	gender = sql.Column(sql.String(12), nullable = False)
	room_id = sql.Column(sql.String(40), nullable = False)
	image = sql.Column(sql.String(40), nullable = False)
	_password = sql.Column(sql.String(125), nullable = False)
	_is_authenticated = sql.Column(sql.Boolean, default = False)

	@property
	def is_authenticated(self):
		return self._is_authenticated

	@is_authenticated.setter
	def is_authenticated(self, value):
		self._is_authenticated = value

	@property
	def password(self):
		raise AttributeError('Password is not readable')

	@password.setter
	def password(self, value):
		self._password = generate_password_hash(value)

	def check_password(self, password):
		return check_password_hash(self._password, password)

class Message(sql.Model):
	__tablename__ = 'message'
	id = sql.Column(sql.Integer, primary_key = True, autoincrement = True)
	user_id = sql.Column(sql.Integer, sql.ForeignKey('wechatuser.id'))	
	message = sql.Column(sql.Text)
	room = sql.Column(sql.Text)
	user = sql.relationship('WechatUser',backref=sql.backref('messages'))


login_manager = LoginManager()
login_manager.login_view = 'client.login'

@login_manager.user_loader
def load_user(user_id):
	return WechatUser.query.get(int(user_id))

