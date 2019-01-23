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
    # Get the requested meetup

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
