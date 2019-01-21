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
    try:
        data = request.get_json()
        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        password = data["password"]
    except:
        return make_response(jsonify({
            "status": 500,
            "message": "Please provide correct details"
        }), 500)

    # phone = data["phone"]

    if not firstname.strip():
        return make_response(jsonify({"message": "Please enter first name!"}))
    elif validate.valid_length(firstname) is False:
        return make_response(jsonify({"message": "FirstName cannot be less than 4 or more than 30 characters"}))
    elif not lastname.strip():
        return make_response(jsonify({"message": "Please enter last name!"}))
    elif validate.valid_length(lastname) is False:
        return make_response(jsonify({"message": "LastName cannot be less than 4 or more than 30 characters"}))
    elif not email.strip():
        return make_response(jsonify({"message": "Please enter last name!"}))
    elif validate.is_valid_email(email) is False:
        return make_response(jsonify({"message": "Please provide a valid email"}))
    elif not password.strip():
        return make_response(jsonify({"message": "Please enter a password!"}))
    elif validate.is_valid_password(password) is False:
        return make_response(jsonify({"message": "Please provide a valid password!"}))

    if db.get_email(email):
        return make_response(jsonify({"message": "That email exists!"}))
    
    db.save_user(firstname, lastname, email, password)
    return make_response(jsonify({"message": "Successfully registered, you can Login!", "status": 201}), 201)

@ver2.route("/auth/login")
def user_login():
    """Login user endpoint"""
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Please provide login info!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    token = db.login_user(auth.username, auth.password)

    if not token:
        return make_response(jsonify({"message": "Incorrect login details!"}), 401)
    return make_response(jsonify({"message": "Successfully logged in!", "status": 200,"token": token}), 200)
