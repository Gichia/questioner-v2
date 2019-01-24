"""User endpoints"""
from flask import request, jsonify, make_response
from app.api.models.users_model import UserClass
from app.api.utils.validations import Validations
from app.api import ver2

db = UserClass()
validate = Validations()

@ver2.route("/auth/signup", methods=["POST"])
def user_signup():
    """Register new user endpoint"""

    error = ""
    status = 200
    response = {}

    try:
        data = request.get_json()
        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]

        if not firstname.strip():
            error = "Please provide your firstname!"
            status = 400
        elif validate.valid_length(firstname) is False:
            error = "FirstName cannot be less than 3 or more than 30 characters"
            status = 400
        elif not lastname.strip():
            error = "Please provide your lastname!"
            status = 400
        elif validate.valid_length(lastname) is False:
            error = "LastName cannot be less than 3 or more than 30 characters"
            status = 400
        elif not email.strip():
            error = "Please provide an email!"
            status = 400
        elif validate.is_valid_email(email) is False:
            error = "Please provide a valid email!"
            status = 400
        elif not password.strip():
            error = "Please provide a password!"
            status = 400
        elif validate.is_valid_password(password) is False:
            error = "Please provide a stronger password!"
            status = 400
        elif not phone.strip():
            error = "Please provide a phone number!"
            status = 400
        else:
            if db.get_email(email):
                error = "That email exists!"
                status = 409
            else:
                new_user = {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": password,
                "phone": phone
                }

                db.save_user(new_user)
                status = 201
    except:
        error = "Please provide all required details"
        status = 500

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": new_user})
    return jsonify(response), status


@ver2.route("/auth/login")
def user_login():
    """Login user endpoint"""
    error = ""
    status = 200
    token = None
    response = {}

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        error = 'Please provide your login info'
        status = 401

    token = db.login_user(auth.username, auth.password)

    if not token:
        error = 'Incorrect login details!'
        status = 401
    else:
        status = 200

    if error:
        response.update({"status": status, "error": error})
        return jsonify(response), status

    response.update({"status": status, "data": token})
    return jsonify(response), status
