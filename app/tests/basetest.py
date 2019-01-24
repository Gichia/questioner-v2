"""Base Class for our tests"""
import unittest
import json
import psycopg2 as pg2
import os
import jwt
import datetime
from instance.config import Config
from app import create_app
from app.database import db_tables, drop_tables


class BaseTest(unittest.TestCase):
    """Initializes our setUp for tests"""
    def setUp(self):
        """Initializes our app and tests"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.db = pg2.connect(os.getenv("DATABASE_URL"))
        self.curr = self.db.cursor()

    def post(self, url, data):
        """Method for post tests"""
        und_token = jwt.encode({'sub': "petergichia35@gmail.com", "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.SECRET_KEY)
        token = und_token.decode("UTF-8")
        headers = {"x-access-token": token}

        return self.client.post(url, data=json.dumps(data), content_type="application/json", headers=headers)

    def get_items(self, url):
        """Method for get tests"""
        return self.client.get(url)
    
    def delete_email(self, email):
        """Method to delete user email after tests"""
        query = """DELETE FROM app_users WHERE email=%s"""
        self.curr.execute(query, (email,))
        self.db.commit()

    def delete_meetup(self, topic):
        """Method to delete meetups after tests"""
        query = """DELETE FROM meetups WHERE topic=%s"""
        self.curr.execute(query, (topic,))
        self.db.commit()

    def delete_comment(self, comment):
        """Method to delete meetups after tests"""
        query = """DELETE FROM comments WHERE comment=%s"""
        self.curr.execute(query, (comment,))
        self.db.commit()
        
    def tearDown(self):
        """Tear down the app after running tests"""
        self.curr.close()
        self.db.close()
        


if __name__ == '__main__':
    unittest.main()