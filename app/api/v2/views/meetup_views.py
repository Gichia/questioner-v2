"""Meetup Endpoints"""
from flask import request, jsonify, make_response
from app.api.v2.models.users_model import login_required
from app.api.v2.models.meetups_model import MeetupsClass
from app.api.v2.utils.validations import Validations
from app.api.v2 import ver2

validate = Validations()
db = MeetupsClass()

@ver2.route("/meetups", methods=["POST"])
@login_required
def post_meetup(current_user):
    """Register new user endpoint"""
    try:
        data = request.get_json()
        topic = data["topic"]
        location = data["location"]
        happeningOn = data["happeningOn"]
    except:
        return make_response(jsonify({"message": "Please provide all relevant meetup details!"}))

    if not topic.strip():
        return make_response(jsonify({"message": "Please enter topic!"}))
    elif validate.valid_length(topic) is False:
        return make_response(jsonify({"message": "Topic cannot be less than 4 or more than 30 characters"}))
    elif not location.strip():
        return make_response(jsonify({"message": "Please enter location!"}))
    elif validate.valid_length(location) is False:
        return make_response(jsonify({"message": "Location cannot be less than 4 or more than 30 characters"}))
    elif not happeningOn.strip():
        return make_response(jsonify({"message": "Please add a date for the meetup!"}))

    user = dict(
        user_id=current_user[0],
        firstname=current_user[1].strip(),
        lastname=current_user[2].strip(),
        email = current_user[3].strip(),
        createdOn=current_user[4].strip(),
        isAdmin=current_user[5]
    )

    db.post_meetup(user["user_id"], location, topic, happeningOn)
    return make_response(jsonify({"message": "Meetup successfully created!", "status": 201}), 201)
