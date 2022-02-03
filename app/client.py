from flask import render_template, redirect, url_for, session, request, flash
from flask import Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app.database import WechatUser, sql, Message
from functools import wraps
from flask_wtf.csrf import generate_csrf
from logging import getLogger
from .tools import wechat_validate_token
import random
import uuid



images = {
'male': ['avatar0.png','avatar1.png','avatar3.png','avatar5.png','avatar8.png'],
'female': ['female1.png','female2.png','female3.png','female4.png','female5.png'],
}
logger = getLogger('seth')

client = Blueprint('client', __name__)

@client.route('/')
@login_required
def homepage():
	return render_template('homepage.html')

@client.route('/profile')
@login_required
def profile_page():
	return render_template('profile.html')

@client.route('/chat/<roomid>')
@login_required
def chat(roomid):
	messages = Message.query.paginate(1, 15, error_out = False).items
	return render_template('chat.html',room_name=roomid, messages = messages)

@client.route('/login', methods=['POST','GET'])
def login():
	csrf_token = generate_csrf()

	if request.method == 'POST':
		csrf_token = request.form.get('csrf-token')
		username = request.form.get('username')
		password = request.form.get('password')

		logger.info(f'csrf-token: f{csrf_token} \n username: {username}\n password: {password}\n')

		if csrf_token and username and password:
			if wechat_validate_token(csrf_token):
				user = WechatUser.query.filter_by(username = username).first()
				if user:
					user.is_authenticated = True
					sql.session.add(user)
					sql.session.commit()

					login_user(user)

					return redirect(url_for('client.homepage'))
			else:
				logger.warning('CSRF_TOKEN verification failed. this user most be trying to login from another website')
		else:
			logger.warning('User submitted a form programmically without username or password or csrf-token')

		flash('Login Failed. Username or password is invalid')
		return redirect(url_for('client.login'))

	return render_template('login.html', csrf_token = csrf_token)


@client.route('/register', methods=['POST','GET'])
def register():
	if request.method == 'POST':
		csrf_token = request.form.get('csrf-token')
		username = request.form.get('username')
		password = request.form.get('password')
		gender = request.form.get('gender')

		logger.info(f'csrf-token: f{csrf_token} \n username: {username}\n password: {password}\n')

		if csrf_token and username and password and (gender in ['male','female']):
			if wechat_validate_token(csrf_token):
				new_user_entry = WechatUser(username = username, gender = gender)
				if gender == 'male':
					new_user_entry.image = random.choice(images['male'])
				else:
					new_user_entry.image = random.choice(images['female'])

				new_user_entry.password = password
				new_user_entry.room_id = 'wechat-' + str(uuid.uuid4())

				sql.session.add(new_user_entry)
				sql.session.commit()
				flash('Login Successful')

				return redirect(url_for('client.login'))
			else:
				logger.warning('CSRF_TOKEN verification failed. this user most be trying to login from another website')
		else:
			logger.warning('User submitted a form programmically without username or password or csrf-token')

		flash('Registration Failed.')
		return redirect(url_for('client.register'))

	csrf_token = generate_csrf()

	return render_template('register.html', csrf_token = csrf_token)

@client.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('client.login'))


