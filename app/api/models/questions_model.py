"""Meetups Model to contain all meetup db operations"""
import datetime
from .basemodel import BaseModel

class QuestionsClass(BaseModel):
    """Class to initiate db and contain common meetup methods"""
    
    def post_question(self, user_id, meetup_id, title, body):
        """Method to post a new meetup"""
        question = {
            "created_by": user_id,
            "meetup_id": meetup_id,
            "title": title,
            "body": body,
            "createdon": datetime.datetime.now()
        }

        query = """INSERT INTO questions (meetup_id, user_id, title, body, createdon) 
                VALUES ( %(created_by)s, %(meetup_id)s, %(title)s, %(body)s, %(createdon)s )"""

        data = self.post_data(query, question)
        return data
