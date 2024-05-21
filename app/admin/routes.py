from wtforms import IntegerField, StringField, TextAreaField
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from flask_login import current_user
from werkzeug.security import generate_password_hash 
from uuid import uuid4

from . import admin_bp
from .. import db, admin_manager
from ..db_model import User, ExamList, ExamQuestions

class UserView(ModelView):
    column_list = ("email", "password", "admin")
    
    def on_model_change(self, form, model, is_created):  
        if is_created:      
            model.user_id = uuid4()
            model.password = generate_password_hash(model.password, method='sha256')
        else:
            model.password = generate_password_hash(model.password, method='sha256')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin
        

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return "<h1>You are not logeed in! </h1>"
        elif current_user.admin:
             return "<h1>You are not admin! </h1>"


class ExamListView(ModelView):
    class ExamListForm(BaseForm):
        exam_id = StringField()
        exam_desc = StringField()

    column_display_pk = True
    create_modal = True
    edit_modal = True

    form = ExamListForm

    def is_accessible(self):        
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return "<h1>You are not logeed in! </h1>"
        elif current_user.admin:
             return "<h1>You are not admin! </h1>"


class ExamQuestionsView(ModelView):
    can_export = True
    column_list = ("index", "question", "exam_id")
    form_overrides = {
        "question":TextAreaField,
        "optiona": TextAreaField,
        "optionb": TextAreaField,
        "optionc": TextAreaField,
        "optiond": TextAreaField,
        "optione": TextAreaField,
        "optionf": TextAreaField,
        "explanation": TextAreaField
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return "<h1>You are not logeed in! </h1>"
        elif current_user.admin:
             return "<h1>You are not admin! </h1>"


admin_manager.add_view(UserView(User, db.session))
admin_manager.add_view(ExamListView(ExamList, db.session))
admin_manager.add_view(ExamQuestionsView(ExamQuestions, db.session))

