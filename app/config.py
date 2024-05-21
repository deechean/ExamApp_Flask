import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') #os.urandom(24)
	CERF_ENABLED = (os.environ.get('CERF_ENABLED')=="True")
	
	# Flask Mail Configuration
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = os.environ.get('MAIL_PORT')
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')	
	MAIL_USE_TLS = (os.environ.get('MAIL_USE_TLS')=="True")
	MAIL_USE_SSL = (os.environ.get('MAIL_USE_SSL')=="True")
	FLASKY_MAIL_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')	
	MAIL_MAX_EMAILS = os.environ.get('MAIL_MAX_EMAILS')
	MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
	
	#FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	# FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	
	# Flask SQLalchemy configuration
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
	
	# Flask User configuration
	USER_ENABLE_EMAIL = os.environ.get('USER_ENABLE_EMAIL')
	USER_APP_NAME = os.environ.get('USER_APP_NAME')
	USER_AFTER_REGISTER_ENDPOINT = os.environ.get('USER_AFTER_REGISTER_ENDPOINT')
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') 

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
	}
