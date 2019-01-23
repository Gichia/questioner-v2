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

    message = ''
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
            message = "Please provide your firstname!"
            status = 200
        elif validate.valid_length(firstname) is False:
            message = "FirstName cannot be less than 4 or more than 30 characters"
            status = 200
        elif not lastname.strip():
            message = "Please provide your lastname!"
            status = 200
        elif validate.valid_length(lastname) is False:
            message = "LastName cannot be less than 4 or more than 30 characters"
            status = 400
        elif not email.strip():
            message = "Please provide an email!"
            status = 400
        elif validate.is_valid_email(email) is False:
            message = "Please provide a valid email!"
            status = 400
        elif not password.strip():
            message = "Please provide a password!"
            status = 400
        elif validate.is_valid_password(password) is False:
            message = "Please provide a stronger password!"
            status = 400
        elif not phone.strip():
            message = "Please provide a phone number!"
            status = 400
        else:
            if db.get_email(email):
                message = "That email exists!"
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
                message = "Succesfully registered, you can now login!"
                status = 201
    except:
        message = "Please provide correct details"
        status = 500

    response.update({"status": status, "message": message})
    return jsonify(response), status


@ver2.route("/auth/login")
def user_login():
    """Login user endpoint"""
    message = ''
    status = 200
    token = None
    response = {}

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        message = 'Please provide your login info'
        status = 401

    token = db.login_user(auth.username, auth.password)

    if not token:
        message = 'Incorrect login details!'
        status = 401
    else:
        message = 'Successfully logged in!'
        status = 200

    response.update({"status": status, "message": message, "token": token})
    return jsonify(response), status
