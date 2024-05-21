from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter, login_required, current_user
from flask_mail import Message
from flask import current_app, render_template, request, get_flashed_messages, session, \
    redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_bp
from .. import db, user_manager, mail
from ..db_model import User
from ..db_utils import is_safe_url


@login_bp.route("/testmail")
def testmail():
	print("-----------------------------------")
	print("CERF_ENABLED", current_app.config["CERF_ENABLED"])
	print("MAIL_SERVER", current_app.config["MAIL_SERVER"])
	print("MAIL_PORT", current_app.config["MAIL_PORT"])
	print("MAIL_USERNAME", current_app.config["MAIL_USERNAME"])
	print("MAIL_PASSWORD", current_app.config["MAIL_PASSWORD"])
	print("MAIL_USE_TLS", current_app.config["MAIL_USE_TLS"])
	print("MAIL_USE_SSL", current_app.config["MAIL_USE_SSL"])
	print("-----------------------------------")
	msg = Message("Test mail from ExamApp", recipients=['deechean@gmail.com'])
	msg.html = "<b>This is an HTML message!</b>"
	mail.send(msg)
	return "<h1>Mail sent out.</h1>"

#login_manager.login_view = "login_bp.login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.filter_by(user_id=user_id).first()

# @login_bp.route("/login", methods=["GET", "POST"])
# def login():
#     user = None
#     error = None
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
#         remember_me = request.form.get("remember_me")
#         user = User.query.filter_by(email=email).first()
#         if user:
#             login_user(user, remember=remember_me)
#             if check_password_hash(user.password, password):    
#                 print("POST",session["next"])
#                 if "next" in session and session["next"]: 
#                     if is_safe_url(session["next"]):
#                         return redirect(session["next"])           
                
#                 return redirect(url_for("browse_bp.index"))
#             else:                
#                 error = "The password is incorrect!"
#         else:
#             error = "The user account is not existed!"             
    
#     session["next"] = request.args.get("next")
#     print("GET",session["next"] )
#     return render_template("login.html", current_user=current_user, error=error)

# @login_bp.route("/register", methods=["GET", "POST"])
# def register():    
#     return "<h1>This is register page.</h1>"

# @login_bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return "<h1>This is logout page.</h1>"
