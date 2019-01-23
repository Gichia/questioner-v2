"""Meetup Endpoints"""
from flask import request, jsonify, make_response
from app.api.models.users_model import login_required
from app.api.models.meetups_model import MeetupsClass
from app.api.utils.validations import Validations
from app.api import ver2

validate = Validations()
db = MeetupsClass()

@ver2.route("/meetups", methods=["POST"])
@login_required
def post_meetup(current_user):
    """Register new user endpoint"""
    message = ''
    status =200
    response = {}
    
    try:
        data = request.get_json()
        topic = data["topic"]
        location = data["location"]
        happeningOn = data["happeningOn"]
        tags = data["tags"]

        if not location.strip():
            message = "Please provide a location!"
            status = 400
        elif validate.valid_length(location) is False:
            message = "Location cannot be less than 4 or more than 30 characters"
            status = 400
        elif not topic.strip():
            message = "Please provide a topic!"
            status = 400
        elif validate.valid_length(topic) is False:
            message = "Topic cannot be less than 4 or more than 30 characters"
            status = 400
        elif not happeningOn.strip():
            message = "Please provide a date for the meetup!"
            status = 400
        elif current_user[5] is False:
            message = "Requires Admin Login!"
            status = 401
        else:
            user = dict(
                user_id=current_user[0],
                firstname=current_user[1].strip(),
                lastname=current_user[2].strip(),
                email = current_user[3].strip(),
                createdOn=current_user[4].strip(),
                isAdmin=current_user[5]
            )

            db.post_meetup(user["user_id"], location, topic, happeningOn, tags)
            message = "Meetup succesfully created!"
            status = 201
    except:
        message = "Please provide all the required fields!"
        status = 500


    response.update({"status": status, "message": message})
    return jsonify(response), status

@ver2.route("/meetups/<int:meetup_id>", methods=["GET"])
def get_singel_meetup(meetup_id):
    """Endpoint to get specific meetup"""
    message = ''
    status = 200
    response = {}

    meetup = db.get_single_meetup(meetup_id)
    
    if not meetup:
        message = 'Meetup not found!'
        status = 404
    else:
        message = 'Succesfull!'
        status = 200

    response.update({"status": status, "message": message, "meetup": meetup})
    return jsonify(response), status


@ver2.route("/meetups", methods=["GET"])
def get_meetups():
    """Endpoint to get all meetups"""
    meetups = db.get_meetups()

    return jsonify({"message": "All meetups", "status": 200, "meetups": meetups}), 200
