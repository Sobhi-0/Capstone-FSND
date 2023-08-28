# Capstone-FSND
Project Casting Agency Site -- Final project to complete the Full Stack Nanodegree from Udacity


In the application you can:
1. Dispaly Actors/Movies
2. Delete Actors/Movies
3. Add new Actors/Movies
4. Edit existing Actors/Movies

We are always working on enchancing the users' experience and we are always welcoming your improvments.

## Want to fix a bug? Or perhaps, add a feature?

If you are intrested in contributing into improving our application then kindly read the following:
- Follow the PEP8 style guide
- Our API follows the RESTFull principles

## Dependancies

-Python 3

To install the ```requirements``` , in the root directory run ```pip install -r requirements.txt```

### Backend

To run the application locally
Note: you can create a local Postgres database for the main app to run using the command ```createdb capstone``` and update the URI for the database in the code, you MUST have a local database for tests(test_app.py), use the command ```createdb capstone_test```.

Note 2: On the first run in ```app.py``` uncomment these two lines:
```python
with app.app_context():
   db_drop_and_create_all()
```

In the root directory run the following commands:
bash:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload`
```
===================================
or PowerShell:
```PS
$env:FLASK_APP="app.py"
$env:FLASK_DEBUG="true"
flask run --reload`
```

If you get an error ```ModuleNotFoundError``` instead of running ```flask run --reload``` try running ```python -m flask run``` this can help ensure that Python treats the project_directory as the root directory for imports.

## API Documentation

### Getting Started
Base URL (hosted on Render): ```######################``` || (while running locally) :  ```https://localhost:5000/```

Authentication
-
There is three roles in this application and it is required to have the apropiate role to use the endpoints.
Roles:
-
    Casting Assistant:
        Can view actors and movies
    Casting Director:
        All permissions a Casting Assistant has and…
        Add or delete an actor from the database
        Modify actors or movies
    Executive Producer:
        All permissions a Casting Director has and…
        Add or delete a movie from the database

You need to set the environment variable to use with your Bearer token:
bash:
```bash
export TOKEN=YOUR_TOKEN
```
or PowerShell:
```PS
$env:TOKEN=YOUR_TOKEN
```

### Error Handling
We are using HTTP response codes to indicate the success or failure of an API request. The responses are formated in JSON indicating that a failure happend and showing the error code and message.

Example:

```JSON
{
    'success': False,
    'error_code': 404,
    'message': 'resource not found'
}
```

Errors that might be returned:
-400: Bad Request
-404: Resource Not Found
-405: Method Not Allowed
-422: Not Processable

### Endpoint Library

GET /actors | GET /movies
-
The response indicates the succes of the request and retreaves a list of all actors/movies paginated and limited to 10 actors/movies per page.
- Request Arguments: (optional) ```/?page=<page_number>```
- Returns: The list of actors/movies with a maximum of 10 actors/movies each actor with (id, name, gender, age), each movie with (id, title, release_date)
Total number of actors/movies
Current page number

Request URL example:

```bash
curl -H "Authorization: Bearer $TOKEN" ######################/movies?page=2
```

Response Example:
```JSON
{
  "current_page": 2,
  "movies": [
    {
      "id": 11,
      "release_date": "Fri, 11 Jun 1993 00:00:00 GMT",
      "title": "Jurassic Park"
    },
    {
      "id": 12,
      "release_date": "Fri, 18 Dec 2009 00:00:00 GMT",
      "title": "Avatar"
    }
  ],
  "success": true,
  "total_movies": 17
}
```

DELETE /actor/<actor_id> | DELETE /movie/<movie_id>
-
Deletes the actor/movie of the given ID
- Request Arguments: ```/<id>```
- Returns: ID of the deleted ID with the total number of remaining items

Request URL example:

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" ######################/movies/5
```

Response Example:

```JSON
{
  "deleted": "5",
  "success": true,
  "total_movies": 16
}
```

POST /actors | POST /movies
-
Add a new actor/movie
- Request Arguments:
    for a new actor: name, gender, age
    for a new movie: title, release_date
- Returns: The added item id and the updated total number of existing items

Request URL example:

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name": "Leonardo DiCaprio", "age": 48, "gender": "Male"}' ######################/actors
```

Response Example:

```JSON
{
  "added": 18,
  "success": true,
  "total_movies": 17
}
```

PATCH /actor/<actor_id> | PATCH /movie/<movie_id>
Updates an existing actor/movie partially
- Request Arguments (at least one of the following):
    for a new actor: name, gender, age
    for a new movie: title, release_date
- Returns: The updated item

Request URL example:

```bash
curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"age": 22}' ######################/actors/3
```

Response Example:

```JSON
{
  "success": true,
  "updated": {
    "age": 22,
    "gender": "Male",
    "id": 3,
    "name": "Some actor"
  }
}
```
