import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import Actor, Movie, db


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        self.db = db


        # Populate the database with test data
        movie1 = Movie(title='Movie 1', release_date='2022-01-01')
        movie2 = Movie(title='Movie 2', release_date='2022-02-01')
        actor1 = Actor(name='Actor 1', age=30, gender='Male')
        actor2 = Actor(name='Actor 2', age=25, gender='Female')
    
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

    # Test the "/actors" endpoint to handle GET requests
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)   
        # Make sure the response is correct
        self.assertTrue(len(data['actors']))  
        self.assertTrue(data['total_actors'])  
        self.assertTrue(data['current_page'])  

    # Test the "/movies" endpoint to handle GET requests
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)      
        # Make sure the response is correct
        self.assertTrue(len(data['movies']))  
        self.assertTrue(data['total_movies'])  
        self.assertTrue(data['current_page'])  


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
