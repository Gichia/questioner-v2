"""Base Class for our tests"""
import psycopg2 as pg2
import os
import unittest
import json
from app import create_app
from app.database import db_tables, drop_tables


class BaseTest(unittest.TestCase):
    """Initializes our setUp for tests"""
    def setUp(self):
        """Initializes our app and tests"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.db = pg2.connect(os.getenv("TEST_DATABASE_URL"))
        curr = self.db.cursor()
        tables = db_tables()

        for query in tables:
            curr.execute(query)
        self.db.commit()

    def post(self):
        pass


    def get(self):
        pass
        

    def tearDown(self):
        """Tear down the app after running tests"""
        self.app = None
        curr = self.db.cursor()
        tables = drop_tables()
        
        for query in tables:
            curr.execute(query)
        self.db.commit()


if __name__ == '__main__':
    unittest.main()