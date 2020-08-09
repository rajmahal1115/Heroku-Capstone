import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random
import datetime

from app import create_app
from models import setup_db, Actor, Movie, Gender
from auth  import AuthError, requires_auth


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        
        self.database_name = "castingAgency_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:Narnarayan@localhost:5432', self.database_name)
        self.app = create_app({"DATABASE_URL":self.database_path})
        self.client = self.app.test_client


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            for x in range(0,3):
                self.createActors()
                self.createMovies()
        
        self.casting_assistant = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJb0wwQkNXS0lqdF9vU1gyczFzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi0zanY0YmswNS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMzcyNDYzMmNlYTMwMjIxMTQxNTkwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY5ODgwODMsImV4cCI6MTU5NzA3NDQ4MywiYXpwIjoiVzU3T1V3TXJoM2h6emx1a0FiREtBTzEweVppQVd4UjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.f9gac23KuxweDnXjdd8ij_15UbMVVgASbUZlU4MWElSiKUzqXKN9Ota6p10oiI8CfFhaW7sBGG9Gp7G8qfx7-iXIAOHxPkxXwQszYL_zEfh5UxthekUVXRo7yMDch3h1rtfU_p7l6Qt0sWj7CC_2tSD1KJmpmChzBv194SPPIKK7fo0FtT0n5sUSpCafUTl9tNMisRQKyXY1tVlyq71CG5ZHEGv2Vcu92tvKYFZpwxtp05hSojHMiY1G-ss-u_5SFsSxuNAfpGzGJOJio9-pVFaLYuSMpVneS05QkfKC0uWCXXt9nDrv8txeEhq1WyM974-dV3RX3Ej3n3ygQ4wEUg')

        self.casting_director = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJb0wwQkNXS0lqdF9vU1gyczFzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi0zanY0YmswNS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMzcyMjVkYzY4MjYwMGEwYjYzYzM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY5OTA3MzMsImV4cCI6MTU5NzA3NzEzMywiYXpwIjoiVzU3T1V3TXJoM2h6emx1a0FiREtBTzEweVppQVd4UjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.fN6UaprJs7xZL9ja00tpOwabUfVycLBySEH1Qno63N_Gjk-6bjrNy5uZXplc0WxF4oM9ZwjbZnO3fEC2VgBlpI3LXzNgHcwRkiPu6iUHByUMETR6-AnKW3ddXqhBvmhTWMCCsJKNy9aciWvjK4-ERI3WXNDcTLB9qHiYa4ObnrrJFNsHNjj-VVIaT0iVz6jbbAHRAcJipx1Jp_4arN421BZ11w74i_uhB8d3ze_2Bf6X4Vsd1CmOumsI7_5QjAxzgTRgn2VrFgP7OfxfYfG9ZezUKwMmpYVLS88VgcoBWBcX3dFhG3JrppKZ6pKIXaHaeA08TOQ2z_xMXEUMcsgcyg')

        self.executive_producer = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJb0wwQkNXS0lqdF9vU1gyczFzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi0zanY0YmswNS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMzcyYjc1Yzg0OGYwMDM3YzQyODE5IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY5OTEyODQsImV4cCI6MTU5NzA3NzY4NCwiYXpwIjoiVzU3T1V3TXJoM2h6emx1a0FiREtBTzEweVppQVd4UjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.10HtdU3Uzkwu1f7bpZPihNrfIwOLpFlbIxKvn_JQ6eMw3Esh5THJGpR5_zBXXVjqCMuu7cGwC-W60JgDupr42Bk1mKPMG336m6Ta9l7vik6oSBAvw8fCPpXIDO5aVQqsxWRrwAUisR6VZqbIiU2p6LTDaFgl5iqbokboRfHr14TRYpGYy5_UtrZ7hsPnL6FAFoSwFLhQhN_bRA6gUx0YypbDYunbjBDGTZ0s9-8lwI8nvY0oaS5jrJYoUEcHEyMRZoAfJWigN3iHAt9DV3JjEpyzvPEc7vUxyXxyMHu2PtxhCEdwc-AKUB5dwI5mrMrM9jPuZlkCuoDj4GKWEcW2mA')

        self.expired_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJb0wwQkNXS0lqdF9vU1gyczFzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi0zanY0YmswNS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMzcyYjc1Yzg0OGYwMDM3YzQyODE5IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY0MDIyMjcsImV4cCI6MTU5NjQ4ODYyNywiYXpwIjoiVzU3T1V3TXJoM2h6emx1a0FiREtBTzEweVppQVd4UjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.OhJ3xdgiAt7F3ubHyHbOu5Q1HsSiKnqgIFEhMNpqhM_byugUTZ7Qt6U_kV1_IE6-9ePCgGp3qOkirtw6XnffWN879yaXMcrdMfkwgwiOIVJwLalArBdytr_LhE9hubLjWpxKulszc7Jtv-2Yu4Ew6Z3GpXKu3ZTN3uhKpSeU7OIIEHqpz8IzXFHc5xUFWQPTYoSyUd27M3_5SG0O2s6Y6KF8OUsuQhlkvxpn6wjTL45LTMUKjMO2dpmq447aKoGuzrRK69HOzRv9Q02zsYOPFgaKUUTLMqbHDnhq-Ol2U-DWjcSlJEQL1NIUc8TTJVMbj5eKJT9TUj7SgzMSTBMm7A')

    def tearDown(self):
        pass

    def createActors(self):
        if Actor.query.count() < 3:
            genders = [Gender.Male,Gender.Female,Gender.Unknown]
            age = random.randrange(20,100)
            gender = random.choice(genders)

            actor = Actor(name = "test actor",
                          age = age,            
                          gender = gender)
            actor.insert()
            
    def createMovies(self):
        if Movie.query.count() < 3:
            ReleaseDates = [datetime.datetime(2017, 6, 1),
                    datetime.datetime(2018, 7, 1),
                    datetime.datetime(2019, 6, 1)]
            releaseDate = random.choice(ReleaseDates)
            movie = Movie(title = "testing movie",
                          releaseDate = releaseDate)
            movie.insert()
    
    # getting single actor test
    def test_get_actor(self):
        actor_to_get = Actor.query.first()
        res = self.client().get(f'/actors/{actor_to_get.id}',headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
    
    # getting single actor test fail
    def test_get_actor_fail(self):
        res = self.client().get('/actors/100000',headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)

    #getting all actors test
    def test_get_actors(self):
        res = self.client().get('/actors',headers={
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data['actors']))
    

    #getting all movies test
    def test_get_movies(self):
        res = self.client().get('/movies',headers={
            'Authorization': self.casting_director
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data['movies']))

    
    #deleting a single actor by id test
    def test_delete_actors(self):
        actor_to_delete = Actor.query.first()
        res = self.client().delete(f'/actors/{actor_to_delete.id}',headers={
            'Authorization': self.casting_director
        })
        data = json.loads(res.data)

        actor = Actor.query.filter(
            Actor.id == actor_to_delete.id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'],'Success')
        self.assertEqual(actor, None)

    #deleting a single actor by id test fail
    def test_delete_actors_fail(self):
        res = self.client().delete('/actors/100000',headers={
            'Authorization': self.casting_director
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'],'Failure')


    #delete a single movie by id test
    def test_delete_movies(self):
        movie_to_delete = Movie.query.first()
        res = self.client().delete(f'/movies/{movie_to_delete.id}',headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        movie = Movie.query.filter(
            Movie.id == movie_to_delete.id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'],'Success')
        self.assertEqual(movie, None)

    #delete a single movie by id test fail
    def test_delete_movies_fail(self):
        res = self.client().delete('/movies/1000000',headers={
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'],'Failure')

    #adding an actor test
    def test_create_actors(self):
        res = self.client().post('/actors',json={
            "name":"Jar Letap",
            "age": 65,
            "gender": "Male"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['status'],'Success')

    
    #adding an actor test fail
    def test_create_actors_fail(self):
        res = self.client().post('/actors',json={
            "name":"Failed Test"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['status'],'Failure')

    #adding an movie test
    def test_create_movies(self):
        res = self.client().post('/movies',json={
            "title":"Young Masala",
            "releaseDate": "1991-11-15"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['status'],'Success')
    
    #adding an movie test fail
    def test_create_movies_fail(self):
        res = self.client().post('/movies',json={
            "title":"Young Masala"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['status'],'Failure')

    #updating an actor test
    def test_update_actors(self):
        actor_to_update = Actor.query.first()
        res = self.client().patch(f'/actors/{actor_to_update.id}',json={
            "name":"Young Dre 1st"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['status'],'Success')


    #updating an actor test fail
    def test_update_actors_fail(self):
        res = self.client().patch('/actors/100000',json={
            "name":"Young Dre 1st"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['status'],'Failure')
        


    #updating a movie test 
    def test_update_movies(self):
        movie_to_update = Movie.query.first()
        res = self.client().patch(f'/movies/{movie_to_update.id}',json={
            "title":"Young Masala2",
            "releaseDate": "1991-11-15"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['status'],'Success')


    #updating a movie test fail 
    def test_update_movies_fail(self):
        res = self.client().patch('/movies/1000000',json={
            "title":"Young Masala Fail"
        },headers = {
            'Authorization': self.executive_producer
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['status'],'Failure')
    
    
    def test_no_authorization(self):
        res = self.client().patch('/movies/1000000',json={
            "title":"Young Masala Fail"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,401)
    
    
    def test_incorrect_permission(self):
        res = self.client().patch('/movies/1000000',json={
            "title":"Young Masala Fail"
        },headers = {
            'Authorization': self.casting_assistant
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,401)

    def test_expired_token(self):
        res = self.client().patch('/movies/1000000',json={
            "title":"Young Masala Fail"
        },headers = {
            'Authorization': self.expired_token
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,401)
       

    def test_invalid_token(self):
        res = self.client().patch('/movies/1000000',json={
            "title":"Young Masala Fail"
        },headers = {
            'Authorization': 'abcdefg'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,401)

    
if __name__ == "__main__":
    unittest.main()


    


            




              
        



