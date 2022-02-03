import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Basic:
	SECRET_KEY = 'basic'
	SQLALCHEMY_TRACK_MODIFICATIONS = True


class Development(Basic):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'database.db')

configurations = {
	'development': Development,
}