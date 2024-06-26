from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(db.Model, UserMixin):
    __table_args__= {"schema":"examapp"}
    __tablename__ = "tb_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False, )
    admin = db.Column(db.Boolean(50), nullable=False, )
    active = db.Column(db.Boolean(), nullable=False, server_default="0")
    confirmed_at = db.Column(db.DateTime())
    usernotes = db.relationship("UserNotes", backref = "tb_user", lazy = "dynamic")

    def __repr__(self):
         return "<User %r>"%(self.username)
    
    # def get_id(self):
    #     return self.id

class ExamList(db.Model):
    __table_args__= {"schema":"examapp"}
    __tablename__ = "tb_exam_list"
    exam_id = db.Column(db.String(50), primary_key=True)
    exam_desc = db.Column(db.String(100))
    questions = db.relationship("ExamQuestions", backref = "tb_exam_list", lazy = "dynamic")

    def __repr__(self):
        return "<ExamList %r>"%(self.exam_id)

class ExamQuestions(db.Model):
    __table_args__= {"schema":"examapp"}
    __tablename__ = "tb_exam_questions"
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=True)
    question = db.Column(db.String(500))
    optiona = db.Column(db.String(300))
    optionb = db.Column(db.String(300))
    optionc = db.Column(db.String(300))
    optiond = db.Column(db.String(300))
    optione = db.Column(db.String(300))
    optionf = db.Column(db.String(300))
    correct_ans = db.Column(db.String(300))
    explanation = db.Column(db.String(1000))
    exam_id = db.Column(db.String(50), db.ForeignKey(ExamList.exam_id), nullable=False)
    ansnum = db.Column(db.Integer, nullable=True)
    usernotes = db.relationship("UserNotes", backref = "tb_exam_questions", lazy = "dynamic")

    def __repr__(self):
        return "<ExamQuestions %r %r>"%(self.exam_id, self.index)
    
class UserNotes(db.Model):
    __table_args__= {"schema":"examapp"}
    __tablename__ = "tb_usernotes"
    note_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(ExamQuestions.id), nullable=True)
    category = db.Column(db.String(300))
    notes = db.Column(db.String(1000))
    my_ans = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    highlightnotes = db.relationship("HighlightNotes", backref = "tb_usernotes", lazy = "dynamic")

class HighlightNotes(db.Model):
    __table_args__= {"schema":"examapp"}
    __tablename__ = "tb_highlightnotes"
    note_id = db.Column(db.Integer, primary_key=True)
    usernote_id =db.Column(db.Integer, db.ForeignKey(UserNotes.note_id), nullable=True)
    column_name = db.Column(db.String(300),  nullable=True)
    start_pos = db.Column(db.Integer,nullable=True)
    length = db.Column(db.Integer,nullable=True)
    highlight_color = db.Column(db.String(300), nullable=False)
    highlight_notes = db.Column(db.String(1000))

def get_current_user():
    user = None
    if current_user.is_authenticated: 
        user = User.query.filter(email = current_user.email) 
    return user, current_user.is_authenticated

    