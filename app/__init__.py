from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
#from flask_login import LoginManager
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter, login_required, current_user
from flask_mail import Mail
from .config import config


db = SQLAlchemy()
admin_manager = Admin(template_mode="bootstrap3")
#login_manager = LoginManager()
user_manager = UserManager()
mail = Mail()

def create_app(config_name="production"):
	app = Flask(__name__)	
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)	
    
	#init flask components
	db.init_app(app)
	
	admin_manager.init_app(app)

	#login_manager.init_app(app)

	mail.init_app(app)

	from .db_model import User 
	user_manager.init_app(app, db_adapter= SQLAlchemyAdapter(db, User))

    # Registering blueprints
	from .admin import admin_bp 	    
	app.register_blueprint(admin_bp)
	from .login import login_bp 	    
	app.register_blueprint(login_bp)
	from .browse import browse_bp 	    
	app.register_blueprint(browse_bp)	

	return app
