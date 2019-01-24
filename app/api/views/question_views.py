"""Question endpoints"""
from flask import request, jsonify, make_response
from app.api.models.users_model import login_required
from app.api.models.questions_model import QuestionsClass
from app.api.models.meetups_model import MeetupsClass
from app.api.utils.validations import Validations
from app.api import ver2

db = QuestionsClass()
meet = MeetupsClass()
validate = Validations()

@ver2.route("/questions/<int:meetup_id>", methods=["POST"])
@login_required
def post_question(current_user, meetup_id):
    """ Post question to specific meetup """

    message = ""
    status = 200
    response = {}

    try:
        data = request.get_json()
        title = data["title"]
        body = data["body"]

        if not title.strip():
            message = "Please provide your title!"
            status = 200
        elif validate.valid_length(title) is False:
            message = "Title cannot be less than 4 or more than 30 characters"
            status = 200
        elif not body.strip():
            message = "Please provide your body!"
            status = 200
        elif validate.valid_length(body) is False:
            message = "body cannot be less than 4 or more than 30 characters"
            status = 400
        else:
            data = meet.get_single_meetup(meetup_id)
            if not data:
                message = "Meetup not found!"
                status = 404
            else:
                message = "Succesfully added!"
                status = 201
    except:
        message = "Please provide correct details"
        status = 500

    user_id = current_user[0]
    db.post_question(user_id, meetup_id, title, body)

    question = {
        "title": title,
        "body": body
    }
    response.update({"status": status, "message": message, "data": question})
    return jsonify(response), status

@ver2.route("/questions/<int:meetup_id>", methods=["GET"])
def get_meetup_questions(meetup_id):
    """ Get specific meetup questions"""
    message = ''
    status = 200
    response = {}

    questions = db.get_meetup_questions(meetup_id)

    if questions is None:
        message = "No questions found!"
        status = 404
    else:
        message = "Meetup questions!"
        status = 200

    response.update({"status": status, "message": message, "data": questions})
    return jsonify(response), status

@ver2.route("/questions/upvote/<int:question_id>", methods=["PATCH"])
@login_required
def upvote_question(current_user, question_id):
    """Endpoint to upvote a question"""
    message = ""
    status = 200
    response = {}

    question = db.get_single_question(question_id)

    if not question:
        message = "That question does not exist!"
        status = 404
    elif db.upvote_question(current_user[0], question_id) is False:
        message = "You have already upvoted!"
        status = 400
    else:
        db.upvote_question(current_user[0], question_id)
        message = "Question upvoted!"
        status = 200

    response.update({"status": status, "message": message})
    return jsonify(response), status

@ver2.route("/questions/downvote/<int:question_id>", methods=["PATCH"])
@login_required
def downvote_question(current_user, question_id):
    """Endpoint to upvote a question"""
    message = ""
    status = 200
    response = {}

    question = db.get_single_question(question_id)

    if not question:
        message = "That question does not exist!"
        status = 404
    elif db.downvote_question(current_user[0], question_id) is False:
        message = "You have already downvoted!"
        status = 400
    else:
        db.downvote_question(current_user[0], question_id)
        message = "Question downvoted!"
        status = 200

    response.update({"status": status, "message": message})
    return jsonify(response), status

@ver2.route("/comments/<int:question_id>", methods=["POST"])
@login_required
def comment_question(current_user, question_id):
    """Endpoint to comment on a question"""
    message = ""
    status = 200
    response = {}

    try:
        data = request.get_json()
        comment = data["comment"]
        if not comment.strip():
            message = "Please provide a comment!"
            status = 400
        elif validate.valid_length(comment) is False:
            message = "A comment cannot be less than 4 or more than 30 characters"
            status = 400
        else:
            db.post_comment(current_user[0], question_id, comment)
            message = "Comment succesfully submitted!"
            status = 201
    except:
        message = "Please provide correct details"
        status = 500

    response.update({"status": status, "message": message})
    return jsonify(response), status

    