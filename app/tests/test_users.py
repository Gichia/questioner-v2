"""File to test all meetup endpoints"""
import json
from app.tests.basetest import BaseTest


data = {
    "topic": "Meetup Five",
    "location": "Parklands",
    "happeningOn": "12/12/2018"
    }

class TestUsers(BaseTest):
    """ Class to test all user endpoints """

    def test_user_signup(self):
        """Method to test user signup"""
        response = self.client.post("http://localhost:5000/api/meetups", data=json.dumps(data), content_type="application/json")
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 201)
