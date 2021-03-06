"""File to test all meetup endpoints"""
import os
import psycopg2 as pg2
import json
from app.tests.basetest import BaseTest


data = {
	"topic": "Test Topic",
	"location": "Westlands",
	"happeningOn": "12/12/2020",
	"tags": ["test", "test2"]
}

data2 = {
	"location": "Westlands",
	"happeningOn": "12/12/2020",
	"tags": ["test", "test2"]
}

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

    def test_post_meetup(self):
        """Method to test post meetup endpoint"""
        url = "http://localhost:5000/api/meetups"
        url2 = "http://localhost:5000/api/meetups"

        response = self.post(url, data)
        response2 = self.post(url2, data2)
        response3 = self.client.post(url, data=json.dumps(data), content_type="application/json")

        result = json.loads(response.data.decode("UTF-8"))
        result2 = json.loads(response2.data.decode("UTF-8"))
        result3 = json.loads(response3.data.decode("UTF-8"))

        self.assertEqual(result["status"], 201)
        self.assertEqual(result2["message"], "Please provide all the required fields!")
        self.assertEqual(result3["status"], 401)

    def test_get_specific_meetup(self):
        """Method to test get specific meetup endpoint"""
        query = """SELECT meetup_id FROM meetups WHERE topic=%s"""
        topic = 'Test Topic'
        self.curr.execute(query, (topic,))
        tm = self.curr.fetchone()
        
        url = "http://localhost:5000/api/meetups/{}".format(tm[0])

        response = self.get_items(url)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 200)

        self.delete_meetup("Test Topic")

    def test_get_upcoming(self):
        """Test upcoming meetups"""
        url = "http://localhost:5000/api/meetups/upcoming"

        response = self.get_items(url)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 200)

    def test_meetup_not_found(self):
        """Test correct response for meetup not found"""
        url = "http://localhost:5000/api/meetups/0"

        response = self.get_items(url)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["message"], "Meetup not found!")

    def test_bad_meetup_url(self):
        """Test correct response for wrong meetup url endpoint"""
        url = "http://localhost:5000/api/meetup/0"

        response = self.get_items(url)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["message"], "Resource not found!")
