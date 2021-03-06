"""File to test all meetup endpoints"""
import os
import psycopg2 as pg2
import json
from app.tests.basetest import BaseTest


data = {
	"title": "Test Title",
	"body": "body"
}

comment = {
    "comment": "Comment 1"
}

class TestQuestions(BaseTest):
    """ Class to test all user endpoints """

    def test_post_question(self):
        """Method to test post meetup endpoint"""
        url = "http://localhost:5000/api/questions/1"

        response = self.post(url, data)

        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 201)
        self.assertEqual(result["message"], "Succesfully added!")

    def test_get_questions(self):
        """Test all meetups questions"""
        url = "http://localhost:5000/api/questions/8"

        response = self.get_items(url)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 200)

    def test_meetup_not_found(self):
        """Test correct response for question not found"""
        url = "http://localhost:5000/api/questions/0"

        response = self.post(url, data)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["message"], "Meetup not found!")

    def test_bad_question_url(self):
        """Test correct response for wrong question url endpoint"""
        url = "http://localhost:5000/api/question/0"

        response = self.post(url, data)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["message"], "Resource not found!")

    def test_comment_question(self):
        """Method to test comment question endpoint"""
        url = "http://localhost:5000/api/comments/1"

        response = self.post(url, comment)
        result = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(result["status"], 201)

        self.delete_comment("Comment 1")
