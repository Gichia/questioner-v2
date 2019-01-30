"""File to test all meetup endpoints"""
import os
import psycopg2 as pg2
import json
from app.tests.basetest import BaseTest


db_data = {
	"firstname": "Kennedy",
	"lastname": "Gichia",
	"email": "ken@gmail2.com",
	"password": "Kennny@1",
	"phone": "0706231221"
    }

db_data2 = {
	"firstname": "Kennedy",
	"lastname": "Gichia",
	"password": "Kennny@1",
	"phone": "0706231221"
    }

db_data3 = {
	"firstname": "Kennedy",
	"lastname": "",
	"email": "ken2@gmail.com",
	"password": "Kennny@1",
	"phone": "0706231221"
    }


class TestUsers(BaseTest):
    """ Class to test all user endpoints """

    def test_user_signup(self):
        """Method to test user signup"""
        url = "http://localhost:5000/api/auth/signup"

        response = self.post(url, db_data)
        response2 = self.post(url, db_data2)
        response3 = self.post(url, db_data3)
        
        result = json.loads(response.data.decode("UTF-8"))
        result_2 = json.loads(response2.data.decode("UTF-8"))
        result_3 = json.loads(response3.data.decode("UTF-8"))

        self.assertEqual(result["status"], 201)
        self.assertEqual(result_2["error"], "Please provide all required details")
        self.assertEqual(result_3["error"], "Please provide your lastname!")

        self.delete_email("ken@gmail2.com")
