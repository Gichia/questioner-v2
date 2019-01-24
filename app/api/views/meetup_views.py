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
    error = ""
    status =200
    response = {}
    
    try:
        data = request.get_json()
        topic = data["topic"]
        location = data["location"]
        happeningOn = data["happeningOn"]
        tags = data["tags"]

        if not location.strip():
            error = "Please provide a location!"
            status = 400
        elif validate.valid_length(location) is False:
            error = "Location cannot be less than 4 or more than 30 characters"
            status = 400
        elif not topic.strip():
            error = "Please provide a topic!"
            status = 400
        elif validate.valid_length(topic) is False:
            error = "Topic cannot be less than 4 or more than 30 characters"
            status = 400
        elif not happeningOn.strip():
            error = "Please provide a date for the meetup!"
            status = 400
        elif current_user[5] is False:
            error = "Requires Admin Login!"
            status = 401
        else:
            data = dict(
                user=current_user[0],
                location=location,
                topic=topic,
                happeningOn = happeningOn,
                tags=tags
            )

            db.post_meetup(data["user"], location, topic, happeningOn, tags)
            status = 201
    except:
        error = "Please provide all the required fields!"
        status = 500

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": data})
    return jsonify(response), status

@ver2.route("/meetups/<int:meetup_id>", methods=["GET"])
def get_single_meetup(meetup_id):
    """Endpoint to get specific meetup"""
    error = ""
    status = 200
    response = {}

    data = db.get_single_meetup(meetup_id)
    
    if data:
        meetup = {}
        for meet in data:
            m = {
                "id": meet[0],
                "createdOn": meet[4].strip(),
                "location": meet[2].strip(),
                "topic": meet[3].strip(),
                "images": meet[5],
                "tags": meet[6].strip()
            }
            meetup.update(m)
        status = 200
    else:
        error = 'Meetup not found!'
        status = 404

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": meetup})
    return jsonify(response), status

@ver2.route("/meetups", methods=["GET"])
def get_meetups():
    """Endpoint to get all meetups"""
    error = ""
    status = 200
    response = {}

    data = db.get_meetups()

    if data:
        meetups = []
        for meetup in data:
            meet = {
                "id": meetup["meetup_id"],
                "createdOn": meetup["createdon"].strip(),
                "location": meetup["location"].strip(),
                "topic": meetup["topic"].strip(),
                "images": meetup["images"],
                "tags": meetup["tags"].strip()
            }
            meetups.append(meet)

        status = 200
    else:
        error = "No meetups yet"
        status = 404

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": meetups})
    return jsonify(response), status


@ver2.route("/meetups/upcoming", methods=["GET"])
def get_upcoming_meetups():
    """Endpoint to get all upcoming meetups"""
    error = ""
    status = 200
    response = {}

    data = db.get_meetups()

    if data:
        meetups = []
        for meetup in data:
            meet = {
                "id": meetup["meetup_id"],
                "createdOn": meetup["createdon"].strip(),
                "location": meetup["location"].strip(),
                "topic": meetup["topic"].strip(),
                "images": meetup["images"],
                "tags": meetup["tags"].strip()
            }
            meetups.append(meet)

        status = 200
    else:
        error = "No meetups yet"
        status = 404

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": meetups})
    return jsonify(response), status


@ver2.route("/meetups/rsvp/<int:meetup_id>", methods=["POST"])
@login_required
def meetup_rsvp(current_user, meetup_id):
    """Meetup rsvp endpoint"""
    error = ""
    status =200
    response = {}
    
    try:
        data = request.get_json()
        res = data["response"].lower().strip()
        if (res != "yes" and res != "no" and res != "maybe"):
            error = "Response can only be Yes, No, or Maybe"
            status =400
        elif not db.get_single_meetup(meetup_id):
            error = "No meetup found!"
            status = 404
        else:
            db.meetup_rsvp(current_user[0], meetup_id, res)
            data = {
                "meetup": meetup_id,
                "status": res
            }
            status =200
    except:
        error = "Please provide a response!"
        status = 500

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": data})
    return jsonify(response), status

@ver2.route("/meetups/delete/<int:meetup_id>", methods=["DELETE"])
@login_required
def delete_meetup(current_user, meetup_id):
    """Endpoint to delete a meetup"""
    error = ""
    message = ""
    status =200
    response = {}

    if current_user[5] is False:
        error = "Requires Admin Login!"
        status = 401
    elif not db.get_single_meetup(meetup_id):
        error = "Meetup not found!"
        status = 404
    else:
        db.delete_meetup(meetup_id)
        message = "Meetup deleted!"
        status = 200

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "message": message})
    return jsonify(response), status