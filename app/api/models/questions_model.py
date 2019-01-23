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

    def get_single_question(self, question_id):
        """Method to get specific question"""
        query = """SELECT * FROM questions WHERE question_id=%s"""

        curr = self.db.cursor()
        curr.execute(query, (question_id,))
        result = curr.fetchall()
            
        if len(result) == 0:
            result = None
                
        return result

    def get_meetup_questions(self, meetup_id):
        """Method to get specific meetup questions"""
        query = """SELECT * FROM questions WHERE meetup_id=%s"""

        curr = self.db.cursor()
        curr.execute(query, (meetup_id,))
        results = curr.fetchall()
            
        if len(results) == 0:
            results = None
                
        return results

    def validate_upvote(self, user_id, question_id):
        """Method to validate if user has voted"""
        query = """ SELECT user_id FROM votes WHERE question_id=%s"""

        curr = self.db.cursor()
        curr.execute(query, (question_id,))
        res = curr.fetchone()
        return res


    def upvote_question(self, user_id, question_id):
        """Method to upvote a question"""
        res = self.validate_upvote(user_id, question_id)
        
        if res:
            return False
        else:
            upvote = {
                "user_id": user_id,
                "question_id": question_id,
                "createdon": datetime.datetime.now(),
                "is_like": 1
            }
            
            query = """INSERT INTO votes (user_id, question_id, createdon, is_like) 
                    VALUES ( %(user_id)s, %(question_id)s, %(createdon)s, %(is_like)s )"""

            data = self.post_data(query, upvote)
            return data
