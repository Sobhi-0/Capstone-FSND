import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from auth.auth import AuthError, requires_auth
from database.models import Actor, Movie, db_drop_and_create_all, setup_db

ITEMS_PER_PAGE = 10

def paginate(request, selection):
    # Takes the page number (if not provided takes 1 as a default)
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    # Makes the items in in a usefull dictionary format
    full_list = [item.format() for item in selection]
    current_page = full_list[start:end]

    return current_page, page

def create_app(db_URI="", test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if db_URI:
        setup_db(app, db_URI)
    else:
        setup_db(app)  

    """
    Uncomment these to reset the database
    NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    """
    # with app.app_context():
    #   db_drop_and_create_all()

    CORS(app)

    @app.route('/health')
    def health():
        return "Up and Running!"

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()
        current_actors, current_page = paginate(request, actors)

        # If there is no actors raises 404 error
        if len(current_actors) == 0:
            abort(404)

        try:
            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(actors),
                'current_page': current_page
            })
        except:
            # If anything happened it is propably an internal error
            abort(500)


    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.order_by(Movie.id).all()
        current_movies, current_page = paginate(request, movies)

        # If there is no movies raises 404 error
        if len(current_movies) == 0:
            abort(404)

        try:
           return jsonify({
                'success': True,
                'movies': current_movies,
                'total_movies': len(movies),
                'current_page': current_page
            })
        except:
            # If anything happened it is propably an internal error
            abort(500)


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        # If the actor doesn't exist it raises an error
        if actor is None:
            abort(404)

        try:
            actor.delete()

            actors = Actor.query.all()

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'total_actors': len(actors)
            })
        except:
            # If any error occurs
            abort(422)


    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)

        # If the movie doesn't exist it raises an error
        if movie is None:
            abort(404)

        try:
            movie.delete()

            movies = Movie.query.all()

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'total_movies': len(movies)
            })
        except:
            # If any error occurs
            abort(422)

    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(jwt):
        # gets the nessecary items from the request
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        # To make sure all the fields are provided in the request
        if name is None or age is None or gender is None:
            abort(400)

        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()

            return jsonify({
                'success': True,
                'added': new_actor.id,
                'total_actors': len(Actor.query.all())
            })
        except:
            abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(jwt):
        # gets the nessecary items from the request
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')

        # To make sure all the fields are provided in the request
        if title is None or release_date is None:
            abort(400)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()

            return jsonify({
                'success': True,
                'added': new_movie.id,
                'total_movies': len(Movie.query.all())
            })
        except:
            abort(422)

        
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def edit_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        # If the actor doesn't exist it raises an error
        if actor is None:
            abort(404)

        # gets the nessecary items from the request
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        try:
            # To make sure only the provided fields are updated
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'updated': actor.format()
            })
        except:
            abort(500)


    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def edit_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)

        # If the movie doesn't exist it raises an error
        if movie is None:
            abort(404)

        # gets the nessecary items from the request
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')

        try:
            # To make sure only the provided fields are updated
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                'success': True,
                'updated': movie.format()
            })
        except:
            abort(500)



    """Error handlers for expected errors"""
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404)

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }), 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422)

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500)

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            'success': False,
            'error': error.error,
            'status_code': error.status_code
        }), error.status_code


    return app

app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)

# To handle each Auth
if __name__ == "__main__":
    app.debug = True
    app.run()