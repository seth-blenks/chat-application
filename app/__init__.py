from flask import Flask
from .socketio import socketio
from .client import client
from .database import sql, login_manager
from .config import configurations

def create_app(config):
	app = Flask(__name__)

	app.config.from_object(configurations[config])
	
	socketio.init_app(app)
	login_manager.init_app(app)
	sql.init_app(app)

	app.register_blueprint(client)
	return app
