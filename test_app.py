import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random
import datetime
import os

from app import create_app
from models import setup_db, Actor, Movie, Gender
from auth import AuthError, requires_auth


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(os.environ.get('DATABASE_URL_TEST'))
        self.client = self.app.test_client

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            for x in range(0, 3):
                self.createActors()
                self.createMovies()

        self.casting_assistant = (os.environ.get('ASSISTANT'))

        self.casting_director = (os.environ.get('DIRECTOR'))

        self.executive_producer = (os.environ.get('PRODUCER'))

        self.expired_token = (os.environ.get('EXPIRED_TOKEN'))

    def tearDown(self):
        pass

    def createActors(self):
        if Actor.query.count() < 3:
            genders = [Gender.Male, Gender.Female, Gender.Unknown]
            age = random.randrange(20, 100)
            gender = random.choice(genders)

            actor = Actor(name="test actor",
                          age=age,
                          gender=gender)
            actor.insert()

    def createMovies(self):
        if Movie.query.count() < 3:
            ReleaseDates = [datetime.datetime(2017, 6, 1),
                            datetime.datetime(2018, 7, 1),
                            datetime.datetime(2019, 6, 1)]
            releaseDate = random.choice(ReleaseDates)
            movie = Movie(title="testing movie",
                          releaseDate=releaseDate)
            movie.insert()

    # getting single actor test
    def test_get_actor(self):
        actor_to_get = Actor.query.first()
        res = self.client().get(f'/actors/{actor_to_get.id}', headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    # getting single actor test fail
    def test_get_actor_fail(self):
        res = self.client().get('/actors/100000', headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # getting all actors test
    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    # getting all movies test

    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': self.casting_director
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    # deleting a single actor by id test

    def test_delete_actors(self):
        actor_to_delete = Actor.query.first()
        res = self.client().delete(f'/actors/{actor_to_delete.id}', headers={
            'Authorization': self.casting_director
        })
        data = json.loads(res.data)

        actor = Actor.query.filter(
            Actor.id == actor_to_delete.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'Success')
        self.assertEqual(actor, None)

    # deleting a single actor by id test fail
    def test_delete_actors_fail(self):
        res = self.client().delete('/actors/100000', headers={
            'Authorization': self.casting_director
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 'Failure')

    # delete a single movie by id test

    def test_delete_movies(self):
        movie_to_delete = Movie.query.first()
        res = self.client().delete(f'/movies/{movie_to_delete.id}', headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        movie = Movie.query.filter(
            Movie.id == movie_to_delete.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'Success')
        self.assertEqual(movie, None)

    # delete a single movie by id test fail
    def test_delete_movies_fail(self):
        res = self.client().delete('/movies/1000000', headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 'Failure')

    # adding an actor test
    def test_create_actors(self):
        res = self.client().post('/actors', json={
            "name": "Jar Letap",
            "age": 65,
            "gender": "Male"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'Success')

    # adding an actor test fail

    def test_create_actors_fail(self):
        res = self.client().post('/actors', json={
            "name": "Failed Test"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 'Failure')

    # adding an movie test
    def test_create_movies(self):
        res = self.client().post('/movies', json={
            "title": "Young Masala",
            "releaseDate": "1991-11-15"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'Success')

    # adding an movie test fail
    def test_create_movies_fail(self):
        res = self.client().post('/movies', json={
            "title": "Young Masala"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 'Failure')

    # updating an actor test
    def test_update_actors(self):
        actor_to_update = Actor.query.first()
        res = self.client().patch(f'/actors/{actor_to_update.id}', json={
            "name": "Young Dre 1st"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'Success')

    # updating an actor test fail

    def test_update_actors_fail(self):
        res = self.client().patch('/actors/100000', json={
            "name": "Young Dre 1st"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 'Failure')

    # updating a movie test

    def test_update_movies(self):
        movie_to_update = Movie.query.first()
        res = self.client().patch(f'/movies/{movie_to_update.id}', 
            json={
                "title": "Young Masala2",
                "releaseDate": "1991-11-15"
            }, 
            headers={
                'Authorization': self.executive_producer
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'Success')

    # updating a movie test fail

    def test_update_movies_fail(self):
        res = self.client().patch('/movies/1000000', json={
            "title": "Young Masala Fail"
        }, headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 'Failure')

    def test_no_authorization(self):
        res = self.client().patch('/movies/1000000', json={
            "title": "Young Masala Fail"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_incorrect_permission(self):
        res = self.client().patch('/movies/1000000', json={
            "title": "Young Masala Fail"
        }, headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_expired_token(self):
        res = self.client().patch('/movies/1000000', json={
            "title": "Young Masala Fail"
        }, headers={
            'Authorization': self.expired_token
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_invalid_token(self):
        res = self.client().patch('/movies/1000000', json={
            "title": "Young Masala Fail"
        }, headers={
            'Authorization': 'abcdefg'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
