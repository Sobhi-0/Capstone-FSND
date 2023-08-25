import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import Actors, Movies, db


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        self.db = db


        # Populate the database with test data
        movie1 = Movies(title='Movie 1', release_date='2022-01-01')
        movie2 = Movies(title='Movie 2', release_date='2022-02-01')
        actor1 = Actors(name='Actor 1', age=30, gender='Male')
        actor2 = Actors(name='Actor 2', age=25, gender='Female')
    
        with self.app.app_context():
            movie1.insert()
            movie2.insert()
            actor1.insert()
            actor2.insert()


    def tearDown(self):
        """Executed after reach test"""
        # Drop all tables
        with self.app.app_context():
            self.db.drop_all()
            self.db.session.commit()

    def test_print(self):
        with self.app.app_context():
            data = Movies.query.all()
        print(data)
        self.assertEqual(len(data),2)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
