import json
import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # Add some initial data
    actors = [
        Actor(name='Meryl Streep', age=72, gender='Female'),
        Actor(name='Tom Hanks', age=65, gender='Male'),
        Actor(name='Robert Downey Jr.', age=56, gender='Male'),
        Actor(name='Scarlett Johansson', age=37, gender='Female'),
        Actor(name='Brad Pitt', age=58, gender='Male'),
        Actor(name='Jennifer Lawrence', age=31, gender='Female'),
        Actor(name='Johnny Depp', age=58, gender='Male'),
        Actor(name='Emma Watson', age=31, gender='Female'),
        Actor(name='Denzel Washington', age=66, gender='Male'),
        Actor(name='Gal Gadot', age=36, gender='Female'),
        Actor(name='Chris Hemsworth', age=38, gender='Male'),
        Actor(name='Angelina Jolie', age=46, gender='Female'),
        Actor(name='Will Smith', age=53, gender='Male'),
        Actor(name='Natalie Portman', age=40, gender='Female'),
        Actor(name='Keanu Reeves', age=57, gender='Male'),
        Actor(name='Jennifer Aniston', age=52, gender='Female')
    ]
    for actor in actors:
        actor.insert()

    movies = [
        Movie(title='Inception', release_date='2010-07-16'),
        Movie(title='The Shawshank Redemption', release_date='1994-09-23'),
        Movie(title='Pulp Fiction', release_date='1994-10-14'),
        Movie(title='The Dark Knight', release_date='2008-07-18'),
        Movie(title='Forrest Gump', release_date='1994-07-06'),
        Movie(title='The Matrix', release_date='1999-03-31'),
        Movie(title='The Godfather', release_date='1972-03-24'),
        Movie(title='Star Wars: Episode IV - A New Hope', release_date='1977-05-25'),
        Movie(title='The Lord of the Rings: The Fellowship of the Ring', release_date='2001-12-19'),
        Movie(title='Avengers: Endgame', release_date='2019-04-26'),
        Movie(title='Jurassic Park', release_date='1993-06-11'),
        Movie(title='Avatar', release_date='2009-12-18'),
        Movie(title='E.T. the Extra-Terrestrial', release_date='1982-06-11'),
        Movie(title='Deadp0ool', release_date='2016-02-12'),
        Movie(title='The Lion King', release_date='1994-06-24'),
        Movie(title='The Avengers', release_date='2012-05-04')
    ]
    for movie in movies:
        movie.insert()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
