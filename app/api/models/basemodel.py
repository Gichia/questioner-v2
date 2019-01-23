"""Base model to initiate db operations"""
from psycopg2.extras import RealDictCursor
from app.db_conn import init_connection

class BaseModel:
    """Base model to initiate db"""
    def __init__(self):
        self.db = init_connection()

    def get_email(self, email):
        """Method to check if email exist"""
        query = """SELECT email FROM app_users WHERE email=%s"""

        cursor = self.db.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def get_user(self, email):
        """Method to find single user with email"""
        query = """SELECT * FROM app_users WHERE email=%s"""

        cursor = self.db.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result



    def delete_user(self, email):
        """Method to delete users"""
        user = self.get_user(email)
        if user:
            query = """ DELETE FROM app_users WHERE email=%s""" 

            curr = self.db.cursor()
            curr.execute(query, (email,))
            curr.commit()
            return email   
        

    def post_data(self, query, data):
        """Method to post data to db"""
        curr = self.db.cursor()
        curr.execute(query, data)
        self.db.commit()
        return data
        
    def get_data(self, query):
        """Method to get data from db"""
        curr = self.db.cursor(cursor_factory=RealDictCursor)
        curr.execute(query)
        result = curr.fetchall()
        return result
