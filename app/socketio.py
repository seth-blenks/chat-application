from flask_socketio import SocketIO, join_room, leave_room, disconnect
from flask import request, redirect, url_for
from flask_login import current_user
from app.database import Message, sql, WechatUser
from functools import wraps
import json
from logging import getLogger

def authentication_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if not current_user.is_authenticated:
			disconnect()
		else:
			return f(*args, **kwargs)

	return wrapper

logger = getLogger('seth')

socketio = SocketIO()

@socketio.on('join')
@authentication_required
def handle_message(data):
	logger.info(f'received message to join: {json.dumps(data)}')
	room = data['room']
	join_room(room)
	socketio.emit('info',{'message': 'user has joined room'}, json = True, to = room)

@socketio.on('message')
@authentication_required
def handle_message(data):
	logger.info(f'Received message: {json.dumps(data)}')
	room = data['room']
	message = data['message']

	new_message_entry = Message(message = message, room = room)
	new_message_entry.user = current_user
	sql.session.add(new_message_entry)
	sql.session.commit()

	socketio.emit('message', {'message': message, 'username': current_user.username, 'image': current_user.image},json=True, to=room)

@socketio.on('connect')
@authentication_required
def handle_connection():
	logger.info(f'User connected with id: {request.sid}\nfetching all users of wechat')
	users = [{'room_id': user.room_id, 'username': user.username} for user in WechatUser.query.all()]



@socketio.on('disconnect')
def handle_disconnection():
	logger.info(f'User has been disconnected {request.sid}')
