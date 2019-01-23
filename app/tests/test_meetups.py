"""File to test all meetup endpoints"""
import os
import psycopg2 as pg2
import json
from app.tests.basetest import BaseTest


class TestMeetups(BaseTest):
    """ Class to test all user endpoints """

    def test_get_meetups(self):
        """Method to test user signup"""
        url = "http://localhost:5000/api/meetups"
        url2 = "http://localhost:5000/api/meetup"

        response = self.get_items(url)
        response2 = self.get_items(url2)

        result = json.loads(response.data.decode("UTF-8"))
        result2 = json.loads(response2.data.decode("UTF-8"))

        self.assertEqual(result["status"], 200)
        self.assertEqual(result2["message"], "Resource not found!")
