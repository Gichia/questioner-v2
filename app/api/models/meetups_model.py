"""Meetups Model to contain all meetup db operations"""
import datetime
from .basemodel import BaseModel

class MeetupsClass(BaseModel):
    """Class to initiate db and contain common meetup methods"""
    
    def post_meetup(self, user_id, location, topic, happeningOn, tags):
        """Method to post a new meetup"""
        meetup = {
            "created_by": user_id,
            "location": location,
            "topic": topic,
            "tags": tags,
            "createdon": datetime.datetime.now()
        }

        query = """INSERT INTO meetups (created_by, location, topic, tags, createdon) 
                VALUES ( %(created_by)s, %(location)s, %(topic)s, %(tags)s, %(createdon)s )"""

        data = self.post_data(query, meetup)
        return data

    def get_meetups(self):
        """Method to get meetups"""
        query = """SELECT * FROM meetups"""

        data = self.get_data(query)
        return data
