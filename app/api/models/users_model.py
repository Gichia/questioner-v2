"""User class to store all db methods"""
import datetime
import jwt
from flask import jsonify, request, make_response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from instance.config import Config
from .basemodel import BaseModel


class UserClass(BaseModel):
    """Contains relevant db methods"""
        
    def save_user(self, data):
        """Method to add new user to db"""    
        user = {
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "email": data["email"],
            "created_on": datetime.datetime.now(),
            "username": data["email"].split('@')[:1],
            "phonenumber": data["phone"],
            "password": generate_password_hash(data["password"])
        }

        query = """INSERT INTO app_users (firstname, lastname, email, created_on, username, phonenumber, password) VALUES ( %(firstname)s, %(lastname)s, %(email)s, %(created_on)s, %(username)s, %(phonenumber)s, %(password)s )"""
        
        data = self.post_data(query, user)
        return data

    def login_user(self, email, password):
        """Function to login user and create token"""
        user = self.get_user(email)

        if user:
            user_data = {
                "user_id": user[0],
                "firstname": user[1].strip(),
                "lastname": user[2].strip(),
                "email": user[3].strip(),
                "createdOn": user[4].strip(),
                "isAdmin": user[5],
                "password": user[6].strip()
            }

            if check_password_hash(user_data["password"], password):
                token = jwt.encode({'sub': user_data["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.SECRET_KEY)
                return token.decode("UTF-8")

def login_required(f):
    """A decorated function for login required!"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return make_response(jsonify({"status": 401, "error":"Login required!"}), 401)

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = UserClass().get_user(data["sub"])
        except:
            return make_response(jsonify({"status": 401, "error":"Token is Invalid, Please Login Again!"}), 401)

        return f(current_user, *args, **kwargs)
    return decorated
