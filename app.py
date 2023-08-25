import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from database.models import Actor, Movie, db_drop_and_create_all, setup_db


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

        # If there is no actors raises 404 error
        if len(actors) == 0:
            abort(404)

        try:
            # Makes the list in a usefull dictionary format
            actors_list = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actors_list
            })
        except:
            # If anything happened it is propably an internal error
            abort(500)


    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()

        # If there is no movies raises 404 error
        if len(movies) == 0:
            abort(404)

        try:
            # Makes the list in a usefull dictionary format
            movies_list = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies_list
            })
        except:
            # If anything happened it is propably an internal error
            abort(500)
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
