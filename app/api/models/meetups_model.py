"""Meetups Model to contain all meetup db operations"""
from .basemodel import BaseModel

class MeetupsClass(BaseModel):
    """Class to initiate db and contain common meetup methods"""
    
    def post_meetup(self, user_id, location, topic, happeningOn):
        """Method to post a new meetup"""
        meetup = {
            "created_by": user_id,
            "location": location,
            "topic": topic
        }

        query = """INSERT INTO meetups (created_by, location, topic) 
                VALUES ( %(created_by)s, %(location)s, %(topic)s )"""

        data = self.post_data(query, meetup)
        return data
