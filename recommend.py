import time
import uuid
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from algorithm.svd import RecModel
from database import db
from mydb import Movie, Top_Movies, Ratings, Tracks, Users

bp = Blueprint('recommend', __name__)


@bp.route('/')
def recommend():
    return redirect(url_for('recommend.index'))


@bp.route('/index')
def index():
    # 查询数据库
    topmovies = Top_Movies.query.all()
    # 筛选year最近的4部top部电影
    topmovies_least = sorted(topmovies, key=lambda x: x.year, reverse=True)[:4]
    # 筛选wr值最高的16+12部top电影
    topmovies_wr = sorted(topmovies, key=lambda x: x.wr, reverse=True)[:28]
    # 将其中16部电影分配给轮播图，12部电影分配给热门电影
    topmovies_wr_carousel = topmovies_wr[:16]
    topmovies_wr_hot = topmovies_wr[16:]

    rec = current_app.model.get_top_n_recommendations(1001, 10)
    print(rec)

    return render_template('recommend/index.html', topmovies_least=topmovies_least,
                           topmovies_wr_carousel=topmovies_wr_carousel, topmovies_wr_hot=topmovies_wr_hot)


def get_new_user_ratings():
    rec_model = current_app.model  # 使用 current_app.model
    last_trained = rec_model.get_last_training_timestamp()

    # 如果没有记录上次训练时间，则获取所有评分
    if last_trained is None:
        new_ratings = Ratings.query.all()
    else:
        # # 转换时间戳为 datetime 对象
        # last_trained_date = datetime.fromtimestamp(last_trained)
        # 查询自上次训练以来的新评分
        new_ratings = Ratings.query.filter(Ratings.timestamp > last_trained).all()

    # 转换为所需的格式: [(user_id, movie_id, rating), ...]
    new_ratings_data = [(r.userId, r.movieId, r.rating) for r in new_ratings]
    return new_ratings_data


@bp.route('/for-you')
def foryou():
    # 为你推荐
    user_id = 1001
    recommend_movies = []

    # 检查用户是否有评分历史
    user_ratings = Ratings.query.filter_by(userId=user_id).order_by(Ratings.timestamp.desc()).all()
    if not user_ratings:
        print('here 1 用户没有评分历史')
        recommend_movies = Top_Movies.query.order_by(Top_Movies.wr.desc()).all()[:10]
    else:
        print('here 2 用户有评分历史')

        # 检查是否需要重新训练模型
        last_rating_time = user_ratings[0].timestamp
        rec_model = current_app.model  # 使用 current_app.model

        model_last_trained = rec_model.get_last_training_timestamp()
        # 如果没有记录上次训练时间，则获取所有评分
        if model_last_trained is None:
            print('here 3 没有记录上次训练时间')
            model_last_trained = 0

        if last_rating_time > model_last_trained:
            # 获取新的用户评分数据
            new_ratings = get_new_user_ratings()

            # 重新训练模型
            print('here 3 重新训练模型')
            rec_model.retrain_model(new_ratings)

            # 弹出等待提醒
            flash('here 4 正在为您重新训练模型，请稍后再试')

        # 生成个性化推荐
        print('here 5 生成个性化推荐')
        recommend_movies = rec_model.get_top_n_recommendations(user_id, 10)

        # 根据moviId查询电影信息
        for i in range(len(recommend_movies)):
            movieId = recommend_movies[i][0]
            movie = Movie.query.get(movieId)
            recommend_movies[i] = movie

        genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                  'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    return render_template('recommend/for-you.html', recommend_movies=recommend_movies, genres_list=genres)


@bp.route('/for-you/<string:genre>')
def foryou_movie(genre):
    # 根据类型推荐
    print(genre)
    recommend_movies = []
    movies = Movie.query.filter(Movie.genres.like('%' + genre + '%')).order_by(Movie.vote_average.desc()).all()[:10]
    recommend_movies.extend(movies)
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    return render_template('recommend/for-you.html', recommend_movies=recommend_movies, genres_list=genres)

@bp.route('/track')
def track():
    user_id = 1001
    # 根据用户id查询用户的浏览历史
    tracks = Tracks.query.filter_by(userId=user_id).order_by(Tracks.time.desc()).all()

    movies = []
    # 根据moviId查询电影信息
    for i in range(len(tracks)):
        movieId = tracks[i].movieId
        print(i, movieId)
        movies.append(Movie.query.get(movieId))

    return render_template('recommend/track.html', tracks=movies)


@bp.route('/single')
def single():
    return render_template('recommend/single.html')


@bp.route('/single/<int:movieId>')
def single1(movieId):
    # 记录用户浏览历史
    # 生成唯一的trackId
    trackId = uuid.uuid1()
    track = Tracks(trackId=trackId, userId=1001, movieId=movieId, time=datetime.now())
    db.session.add(track)
    db.session.commit()

    movie = Movie.query.get(movieId)
    print(str(movie.movieId) + movie.title + str(movie.year) + str(movie.vote_average))

    if movie is None:
        return "Movie not found", 404

    # 根据用户id推荐电影
    user_id = 1001
    rec = current_app.model.get_top_n_recommendations(user_id, 10)
    # 根据moviId查询电影信息
    for i in range(len(rec)):
        movieId = rec[i][0]
        rec[i] = Movie.query.get(movieId)
        print(rec[i].title + str(rec[i].movieId))

    return render_template('recommend/single.html', movie=movie, rec=rec)


@bp.route('/manage')
def manage():
    # 查询数据库
    movies = Movie.query.limit(20).all()
    users = Users.query.limit(20).all()
    ratings = Ratings.query.limit(20).all()
    tracks = Tracks.query.limit(20).all()

    return render_template('recommend/manage1.html', movies=movies, users=users, ratings=ratings, tracks=tracks)


@bp.route('/manage-insert')
def manage_insert():
    return render_template('recommend/insert.html')


@bp.route('/manage-update')
def manage_update():
    return render_template('recommend/update.html')


# 将数据库中的评分数据的时间戳全部修改为当前时间
@bp.route('/update-timestamp')
def update_timestamp():
    ratings = Ratings.query.all()
    for rating in ratings:
        rating.timestamp = time.time()
    db.session.commit()
    return 'ok'
