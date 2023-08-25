import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from database.models import Actors, Movies, db_drop_and_create_all, setup_db


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

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
