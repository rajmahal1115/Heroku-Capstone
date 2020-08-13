### Capstone Project : Casting Agency

This project was the final project in the Udacity Nanodegree.The goal was to create the bankend for a Casting Agency application. This project combined everything that was taught in the previous projects which includes: creating a data model using SQLAlchemy, writing endpoints to do CRUD operations and having proper error handling, implementing RBAC,writing unit tests, hosting api on Heroku and making sure to follow PEP-8 coding standards.

### File Structure

- models.py : Contains the Movies and Actors models along with the gender class
- auth.py : Contains all of te authentication logic
- app.py : Contains all of the CRUD operation logic 
- test_app.py : Contains all of the unit tests for the project 
- requirements.txt : Contains all of the required packages for the project. You will need to `pip install -r requirements.txt`
- setup.sh - set up environment variables for linux based machinces 
- setup.bat - set up environment variables for windows 

### Data Model

There are 2 tables in the database: actors and movies. The Actors keeps track of all of the actors. The table has the columns : id (integer), name (string), age (int) and gender (enum). Gender can be Male,Female or Unknown. The Movies table keeps track of all of the movies. It has the columns : id (integer), title (string) and releaseDate (date). Each table has an insert,update, delete and format helper function.  

### Installing dependecies 

Follow instructions to install the correct version of Python for your platform from https://docs.python.org/3/using/index.html 


### Virtual Environment 
 
 In order to keep all of the dependecies for each project seperate, we will be working in a virtual environemnt. Instructions on setting up a virtual enviornement can be found here https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ 

 ```
 python -m venv venv
venv/bin/activate
 ```

### PIP Dependecies 

Once the virtual enviornment is setup and running the dependecies will need to be installed in the root directory using the following command which will download the required packages for the project: 

`pip install -r requirements.txt`

### Setup File

In the setup.sh and setup.bat files there are environment variables set up that are used within the app. In order to run the app on windows run the setup.bat file in the command prompt (at the root folder of the project) and in order to run the app on a linux based machine run the setup.sh file (at the root folder of the project).  

### Local Database Setup

Once your database has been created open up your command prompt/terminal, go to the root directory and run:

```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### Running the server

From within the root directory you can run the server by running the below commands in the command prompt/ terminal. Note for linux based machines change the "set" to "export". Before running the commands make sure to run setup.bat or setup.bat in the root of the project folder to set the enviornment variables.

```
set FLASK_APP=app.py
set FLASK_DEBUG=true
set FLASK_ENV=development
flask run
```
### Heroku

The app is hosted on Heroku and the link to access it is the following: https://stormy-fortress-51211.herokuapp.com

### Roles

There are three roles that are set up inside of Auth0.
- Casting Assistant : Able to view actors and movies
- Casting Director : Able to do everything the casting agent can, add/delete actors and modify actors/movies
- Executive Producer : Able to do everything the previous 2 can and add/ delete movies


### Testing Locally

There is a test_app.py file which was used to test the functionality of the endpoints in the test environment. Similar to when running the app you will need to run setup.bat or setup.sh. In order to test the code a database will have to be created called "castingAgency_test". It is currently set up to go to a database locally. Once that is done you can run the code the following command.

```
python test_app.py
```

 Also there is a POSTMAN collection used to test the following endpoint in the production environment. 

GET '/actors/<int:id>'
GET '/actors'
GET '/movies'
DELETE '/actors/<int:id>' 
DELETE '/movies/<int:id>'
POST '/actors' 
POST '/movies' 
PATCH '/actors/<int:id>' 
PATCH '/movies/<int:id>'

### GET '/actors/<int:id>'

- Request argument: id of actor as an int 
- Roles able to perform action: Casting Assistant,Casting Director, Executive Producer
- Returns: The actor specified by the id 

```
{
    "actor": {
    "age": 65,
    "gender": "Male",
    "id": 1,
    "name": "Hugh Jackman"
  }
}
```

### GET '/actors'

- Request argument: None
- Roles able to perform action: Casting Assistant,Casting Director, Executive Producer
- Returns: All the actors 

```
{
  "actors": [
    {
      "age": 51,
      "gender": "Male",
      "id": 3,
      "name": "Hugh Jackman"
    },
    {
      "age": 51,
      "gender": "Female",
      "id": 4,
      "name": "Jennifer Aniston"
  ]
}
```

### GET '/movies'

- Request argument: None
- Roles able to perform action: Casting Assistant,Casting Director, Executive Producer
- Returns a list of movies

```
{
  "movies": [
    {
      "id": 3,
      "releaseDate": "Fri, 22 Jun 2001 00:00:00 GMT",
      "title": "Fast and Furious"
    },
    {
      "id": 4,
      "releaseDate": "Mon, 10 July 2020 00:00:00 GMT",
      "title": "The Old Guard"
    }
  ]
}
```

### DELETE '/actors/<int:id>'

- Request arguemnt : id of actor as int
- Roles able to perform action: Casting Director, Executive Producer
- Returns a success message if it successfully deleted the actor otherwise returns an error

```
{
  "status": "Success"
}
```

### DELETE '/movies/<int:id>'

-  Request arguemnt : id of a movie as int
- Roles able to perform action: Executive Producer
- Returns a success message if it successfully deleted the movie otherwise returns an error

```
{
  "status": "Success"
}
```

### POST '/actors' 

- Request arguemnt : None
- Roles able to perform action: Casting Director, Executive Producer
- Creates a new actor based on the information provided (name, age, gender) and returns a success message. If new actor is not created correctly then returns an error

```
{
  "status": "Success"
}
```

### POST '/movies'

- Request arguemnt : None
- Roles able to perform action: Executive Producer
- Creates a new movie based on the information provided (release date and title) and returns a success message. If new movie is not created correctly then returns an error

```
{
  "status": "Success"
}
```

### PATCH '/actors/<int:id>'

- Request arguemnt : id of a actor as int
- Roles able to perform the action: Casting Director, Executive Producer
- Modifies the actor based on the id provided. Returns a succcess message and the new modified actor's information. If there is an issue then it returns an error 

```
{
  "actor": {
    "age": 65,
    "gender": "Male",
    "id": 1,
    "name": "Test Actor"
  },
  "status": "Success"
}
```

### PATCH '/movies/<int:id>'

-  Request arguemnt : id of a movie as int
- Roles able to perform the action: Casting Director, Executive Producer
- Modifies the movie based on the id provided. Returns a succcess message and the new modified movie's information. If there is an issue then it returns an error 

```
{
  "movie": {
    "id": 1,
    "releaseDate": "Sun, 17 Nov 1991 00:00:00 GMT",
    "title": "Test Movie"
  },
  "status": "Success"
}
```

### Error Handling

There is error handling that has been implemented as part of the app. For status codes of 400 (Bad Request) ,404 (Not Found), 422 (Unprocessable Entity) , or 500 (Interal Server Error) it will return the following response

```
{
  'status': 'Failure'
}
```

For status code 401 (Unauthorization) below are the responses that you can get back

```
{
  "code": "authorization_header_missing",
  "description": "Authorization header is expected"
}
```

```
{
  "code": "invalid_header",
  "description": "Authorization header must start with Bearer"
}
```

```
{
  "code": "invalid_header",
  "description": "Token not found"
}
```

```
{
  "code": "invalid_header",
  "description": "Authorization header must be Bearer token"
}
```

```
{
  "code": "unauthorized", "description": "Permission not valid"
}
```

```
{
  "code": "token_expired",
  "description": "token is expired"
}
```

```
{
  "code": "invalid_claims",
  "description": "incorrect claims, please check the audience and issuer"
}
```

```
{
  "code": "invalid_header",
  "description": "Unable to parse authentication token."
}
```

```
{
  "code": "invalid_token",
  "description": "invalid token"
}
```

