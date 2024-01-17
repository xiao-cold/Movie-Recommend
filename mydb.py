from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import db


# app = Flask(__name__)


class Movie(db.Model):
    __tablename__ = 'all_movies'
    movieId = db.Column(db.Integer, primary_key=True)
    tmdbId = db.Column(db.Integer)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.String(360))
    poster_path = db.Column(db.String(255))
    director = db.Column(db.String(255))
    cast = db.Column(db.String(255))
    genres = db.Column(db.String(255))
    vote_average = db.Column(db.String(255))

class Action(db.Model):
    __tablename__ = 'top250_Action'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Adiventure(db.Model):
    __tablename__ = 'top250_Adventure'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Animation(db.Model):
    __tablename__ = 'top250_Animation'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Children(db.Model):
    __tablename__ = 'top250_Children'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Comedy(db.Model):
    __tablename__ = 'top250_Comedy'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Crime(db.Model):
    __tablename__ = 'top250_Crime'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Documentary(db.Model):
    __tablename__ = 'top250_Documentary'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Drama(db.Model):
    __tablename__ = 'top250_Drama'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Fantasy(db.Model):
    __tablename__ = 'top250_Fantasy'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Horror(db.Model):
    __tablename__ = 'top250_Horror'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Top_Movies(db.Model):
    __tablename__ = 'top250_movie'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Mystery(db.Model):
    __tablename__ = 'top250_Mystery'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Romance(db.Model):
    __tablename__ = 'top250_Romance'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))



class SciFi(db.Model):
    __tablename__ = 'top250_Sci-Fi'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Thriller(db.Model):
    __tablename__ = 'top250_Thriller'
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    vote_average = db.Column(db.String(255))
    wr = db.Column(db.String(255))

class Ratings(db.Model):
    __tablename__ = 'ratings'
    userId = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(db.Integer)
    rating = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP)

class Users(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

class Tracks(db.Model):
    __tablename__ = 'tracks'
    trackId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    movieId = db.Column(db.Integer, db.ForeignKey('movies'))
    time = db.Column(db.String(255))


    def __init__(self, title, year, rating):
        self.title = title
        self.year = year
        self.rating = rating


    @classmethod
    def create_movie(cls, title, year, rating):
        movie = cls(title=title, year=year, rating=rating)
        db.session.add(movie)
        db.session.commit()
        return movie

    @classmethod
    def get_all_movies(cls):
        return cls.query.all()

    @classmethod
    def get_movie_by_id(cls, movie_id):
        return cls.query.get(movie_id)

    def update(self, title=None, year=None, rating=None):
        if title:
            self.title = title
        if year:
            self.year = year
        if rating:
            self.rating = rating
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# @app.route('/')
# def test():
#     engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4")
#     # 把当前的引擎绑定给这个会话
#     Session = sessionmaker(bind=engine)
#     # 实例化
#     session = Session()
#     # 返回全部符合的结果
#     r2 = session.query(Action.title).filter(Action.year == 1994).all()
#     r3 = session.query(Action.title).filter(Action.title.endswith('冷')).all()
#     print(r2)
#     print(r3)
#     return '0'
#
#
# if __name__ == '__main__':
#     app.run()
