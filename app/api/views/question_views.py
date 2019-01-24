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
    error = ""
    status = 200
    response = {}

    try:
        data = request.get_json()
        title = data["title"]
        body = data["body"]

        if not title.strip():
            error = "Please provide your title!"
            status = 200
        elif validate.valid_length(title) is False:
            error = "Title cannot be less than 4 or more than 30 characters"
            status = 200
        elif not body.strip():
            error = "Please provide your body!"
            status = 200
        elif validate.valid_length(body) is False:
            error = "body cannot be less than 4 or more than 30 characters"
            status = 400
        else:
            data = meet.get_single_meetup(meetup_id)
            if not data:
                error = "Meetup not found!"
                status = 404
            else:
                user_id = current_user[0]
                db.post_question(user_id, meetup_id, title, body)

                question = {
                    "user": user_id,
                    "meetup": meetup_id,
                    "title": title,
                    "body": body
                }
                status = 201
    except:
        error = "Please provide required details"
        status = 500
    
    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": question})
    return jsonify(response), status

@ver2.route("/questions/<int:meetup_id>", methods=["GET"])
def get_meetup_questions(meetup_id):
    """ Get specific meetup questions"""
    error = ""
    status = 200
    response = {}

    questions = db.get_meetup_questions(meetup_id)

    if questions is None:
        error = "No questions found!"
        status = 404
    else:
        status = 200

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": questions})
    return jsonify(response), status

@ver2.route("/questions/upvote/<int:question_id>", methods=["PATCH"])
@login_required
def upvote_question(current_user, question_id):
    """Endpoint to upvote a question"""
    error = ""
    status = 200
    response = {}

    question = db.get_single_question(question_id)

    if not question:
        error = "That question does not exist!"
        status = 404
    elif db.upvote_question(current_user[0], question_id) is False:
        error = "You have already upvoted!"
        status = 400
    else:
        db.upvote_question(current_user[0], question_id)
        votes = db.get_votes(question_id)
        que_details = db.get_question_details(question_id)
        data = {
            "meetup": que_details[0],
            "title": que_details[1].strip(),
            "body": que_details[2].strip(),
            "votes": votes[0]
        }
        status = 200

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": data})
    return jsonify(response), status

@ver2.route("/questions/downvote/<int:question_id>", methods=["PATCH"])
@login_required
def downvote_question(current_user, question_id):
    """Endpoint to downvote a question"""
    error = ""
    status = 200
    response = {}

    question = db.get_single_question(question_id)

    if not question:
        error = "That question does not exist!"
        status = 404
    elif db.downvote_question(current_user[0], question_id) is False:
        error = "You have already downvoted!"
        status = 400
    else:
        db.downvote_question(current_user[0], question_id)
        votes = db.get_votes(question_id)
        que_details = db.get_question_details(question_id)
        data = {
            "meetup": que_details[0],
            "title": que_details[1].strip(),
            "body": que_details[2].strip(),
            "votes": votes[0]
        }
        status = 200

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": data})
    return jsonify(response), status

@ver2.route("/comments/<int:question_id>", methods=["POST"])
@login_required
def comment_question(current_user, question_id):
    """Endpoint to comment on a question"""
    error = ""
    status = 200
    response = {}

    try:
        data = request.get_json()
        comment = data["comment"]
        if not comment.strip():
            error = "Please provide a comment!"
            status = 400
        elif validate.valid_length(comment) is False:
            error = "A comment cannot be less than 3"
            status = 400
        elif not db.get_single_question(question_id):
            error = "Question not found!"
            status = 404
        else:
            db.post_comment(current_user[0], question_id, comment)
            data = {
                "comment": comment,
                "question": question_id
            }
            status = 201
    except:
        error = "Please provide correct details"
        status = 500

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": data})
    return jsonify(response), status

    