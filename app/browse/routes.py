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
from ..db_model import ExamList, ExamQuestions


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
            return render_template(
                "question.html", 
                exam_id=exam_id, 
                exam_desc=exam_desc, 
                question=question, 
                question_count=question_count,
                show_answer = True
            ) 
    return "<h1>The question doesn't exist.</h1>"

@browse_bp.route("/savemynote", methods=["GET", "POST"])
@login_required
def savemynote(): 
    pass