"""Class to include validations"""
import re
import datetime

class Validations:
    """Validation methods"""
    def is_valid_email(self, email):
        """Validate email"""
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is None:
            return False
        return True

    def is_valid_password(self, password):
        """Validate password"""
        if len(password) < 6 and len(password) > 12:
            return False
        if re.match("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$#@&])[A-Za-z0-9$#@&]{6,}", password) is None:
            return False
        return True

    def valid_length(self, phrase):
        """Method to validate length of string"""
        if len(phrase) < 4 or len(phrase) > 30:
            return False

    def is_string(self, phrase):
        """Validate if variable is string only"""
        if isinstance(phrase, str):
            return True
        return False

    def is_numeric(self, phrase):
        """Validate if variable is int only"""
        if isinstance(phrase, int):
            return True
        return False
            
    def is_future_date(self, date):
        """Check if date is a future date"""
        if date > datetime.date.today():
            return True
        else:
            return False
            
