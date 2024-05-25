from uuid import uuid4

from flask import (
    render_template,
    request,
    get_flashed_messages,
    session,
    redirect,
    url_for,
)
from flask_user import current_user, login_required
from . import browse_bp
from .. import db
from ..db_model import ExamList, ExamQuestions, UserNotes


@browse_bp.route("/", methods=["GET"])
def index():
    examlist = ExamList.query.all()
    return render_template("index.html", current_user=current_user, examlist=examlist)


@browse_bp.route("/jumpto/<exam_id>", methods=["POST"])
@login_required
def jumpto(exam_id):
    exam_id = exam_id
    question_id = request.form["ques_id"]
    return redirect(url_for("browse_bp.question", exam_id=exam_id, question_id=question_id))


@browse_bp.route("/question", methods=["GET", "POST"])
@login_required
def question():
    exam_id = request.args.get("exam_id")
    question_id = request.args.get("question_id")

    if request.method == "POST":  
         question_id = request.form["ques_id"]

    question_count = ExamQuestions.query.filter(ExamList.exam_id==exam_id).count()   
    exam = ExamList.query.filter(ExamList.exam_id==exam_id).first()
    if exam:
        exam_id = exam.exam_id
        exam_desc = exam.exam_desc
        question = ExamQuestions.query.filter(
            ExamQuestions.exam_id==exam_id, ExamQuestions.index==int(question_id)
        ).first()
        if question:
            #the question_id in UserNotes is the id of question, not index
            usernotes = UserNotes.query.filter(
                UserNotes.question_id==question.id,
                UserNotes.user_id==current_user.id
                ).first()
            
            return render_template(
                "question.html", 
                exam_id=exam_id, 
                exam_desc=exam_desc, 
                question=question, 
                question_count=question_count,
                show_answer = True, 
                usernotes=usernotes
            ) 
    return "<h1>The question doesn't exist.</h1>"

@browse_bp.route("/savemynote", methods=["POST"])
@login_required
def savemynote():
    exam_id = request.args.get("exam_id")
    question_id = request.args.get("question_id") 
    
    question = ExamQuestions.query.filter(
            ExamQuestions.exam_id==exam_id, ExamQuestions.index==int(question_id)
        ).first()
    
    category = request.form["category"]
    mynotes = request.form["mynotes"]
    if question:
        if question.ansnum > 1: 
            my_ans = request.form.getlist("answer")
            my_ans_str = ""
            for ans in my_ans:
                my_ans_str += ans
        else:
            my_ans_str = request.form.get("answer")
    my_ans_str = my_ans_str.upper()
    usernote = UserNotes.query.filter(
        UserNotes.question_id == question.id, UserNotes.user_id == current_user.id
    ).first()

    if usernote:
        usernote.my_ans = my_ans_str 
        usernote.category = category
        usernote.notes = mynotes
    else:
        usernote = UserNotes(
            note_id=uuid4(),
            question_id=question.id, 
            user_id=current_user.id,
            category=category,
            notes=mynotes,
            my_ans = my_ans_str
        )
        db.session.add(usernote)
    db.session.commit()
    return redirect(url_for("browse_bp.question", exam_id=exam_id, question_id=question_id))
