from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "movie_system"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # Adjust the length as per your requirement
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)

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

# 测试是否连接成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute("show tables")
        print(rs.fetchone())  # (1,)

if __name__ == '__main__':
    app.run()
