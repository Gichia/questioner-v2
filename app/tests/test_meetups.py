"""File to test all meetup endpoints"""
import os
import psycopg2 as pg2
import json
from app.tests.basetest import BaseTest


class TestMeetups(BaseTest):
    """ Class to test all user endpoints """

    def test_get_meetups(self):
        """Method to test get all meetups endpoint"""
        url = "http://localhost:5000/api/meetups"
        url2 = "http://localhost:5000/api/meetup"

        response = self.get_items(url)
        response2 = self.get_items(url2)

        result = json.loads(response.data.decode("UTF-8"))
        result2 = json.loads(response2.data.decode("UTF-8"))

        self.assertEqual(result["status"], 200)
        self.assertEqual(result2["message"], "Resource not found!")

    def test_get_specific_meetup(self):
        """Method to test get specific meetup endpoint"""
        url = "http://localhost:5000/api/meetups/1"
        url2 = "http://localhost:5000/api/meetups/0"
        url3 = "http://localhost:5000/api/meetus/100"

        response = self.get_items(url)
        response2 = self.get_items(url2)
        response3 = self.get_items(url3)

        result = json.loads(response.data.decode("UTF-8"))
        result2 = json.loads(response2.data.decode("UTF-8"))
        result3 = json.loads(response3.data.decode("UTF-8"))

        self.assertEqual(result["status"], 200)
        self.assertEqual(result2["message"], "Meetup not found!")
        self.assertEqual(result3["message"], "Resource not found!")
