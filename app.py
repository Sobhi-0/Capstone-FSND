import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

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
    """
    # with app.app_context():
    #   db_drop_and_create_all()

    CORS(app)

    @app.route('/actors', methods=['GET'])
    def get_actors():
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
    def get_movies():
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
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
