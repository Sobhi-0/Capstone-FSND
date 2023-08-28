import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import Actor, Movie, db, db_drop_and_create_all


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        self.db = db

        # Populate the database with test data
        with self.app.app_context():
            db_drop_and_create_all()

        # Data to be added when test POST endpoints
        self.valid_new_actor = {
            'name': 'Leonardo DiCaprio',
            'age': 48,
            'gender': 'Male'
        }

        self.valid_new_movie = {
            'title': 'Titanic',
            'release_date': '1997-12-19'
        }

        self.invalid_new_actor = {
            'name': 'Leonardo DiCaprio',
            'age': 48
        }

        self.invalid_new_movie = {
            'title': 'Titanic'
        }

        self.edited_actor = {
            'age': 35
        }

        self.edited_movie = {
            'release_date': '2003-12-27'
        }


    def tearDown(self):
        """Executed after reach test"""
        # Drop all tables
        with self.app.app_context():
            self.db.drop_all()
            self.db.session.commit()

    # Test the "/actors" endpoint to handle GET requests
    def test_get_paginated_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Make sure the response is correct
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['current_page'])
    
    # Test for possible error
    def test_404_error_paginating_actors_page_beyond_available(self):
        res = self.client().get('/actors?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # Test the "/movies" endpoint to handle GET requests
    def test_get_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Make sure the response is correct
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['current_page'])

    # Test for possible error
    def test_404_error_paginating_movies_page_beyond_available(self):
        res = self.client().get('/movies?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    # Test for the "/actors" DELETE endpoint and for a possible error
    def test_delete_actor(self):
        actor_id = 2
        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Make sure the response is correct
        self.assertEqual(data['deleted'], str(actor_id))
        self.assertTrue(data['total_actors'])
        # Make sure it was actually deleted from the database
        with self.app.app_context():
            deleted = Actor.query.get(actor_id)
        self.assertEqual(deleted, None)

    def test_404_delete_nonexistent_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
 

    # Test for the "/movies" DELETE endpoint and for a possible error
    def test_delete_movie(self):
        movie_id = 2
        res = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Make sure the response is correct
        self.assertEqual(data['deleted'], str(movie_id))
        self.assertTrue(data['total_movies'])
        # Make sure it was actually deleted from the database
        with self.app.app_context():
            deleted = Movie.query.get(movie_id)
        self.assertEqual(deleted, None)
    
    def test_404_delete_nonexistent_movie(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # Test for the "/actors" POST endpoint and for a possible error
    def test_adding_actor(self):
        res = self.client().post('/actors', json=self.valid_new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])
        self.assertTrue(data['total_actors'])

    def test_405_adding_actor_with_invalid_request(self):
        res = self.client().post('/actors', json=self.invalid_new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


    # Test for the "/movies" POST endpoint and for a possible error
    def test_adding_movie(self):
        res = self.client().post('/movies', json=self.valid_new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])
        self.assertTrue(data['total_movies'])

    def test_405_adding_movie_with_invalid_request(self):
        res = self.client().post('/movies', json=self.invalid_new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    
    # Test for the "/actors" PATCH endpoint and for a possible error
    def test_editing_actor(self):
        actor_id = 5
        res = self.client().patch(f'/actors/{actor_id}', json=self.edited_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_404_patch_nonexistent_actor(self):
        actor_id = 10000
        res = self.client().patch(f'/actors/{actor_id}', json=self.edited_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # Test for the "/movies" PATCH endpoint and for a possible error
    def test_editing_movie(self):
        movie_id = 5
        res = self.client().patch(f'/movies/{movie_id}', json=self.edited_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_404_patch_nonexistent_movie(self):
        movie_id = 10000
        res = self.client().patch(f'/movies/{movie_id}', json=self.edited_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
