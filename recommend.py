from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app import model
from mydb import Movie, Top_Movies

bp = Blueprint('recommend', __name__)


@bp.route('/')
def recommend():
    return redirect(url_for('recommend.index'))


@bp.route('/index')
def index():
    # 查询数据库
    topmovies = Top_Movies.query.all()
    # 筛选year最近的10部top部电影
    topmovies_least = sorted(topmovies, key=lambda x: x.year, reverse=True)[:10]
    # 筛选wr值最高的10部top电影
    topmovies_wr = sorted(topmovies, key=lambda x: x.wr, reverse=True)[:10]

    # 查询年份最近的10部电影的tmdbId，用来匹配海报文件名
    topmovies_least_tmdbId = []
    for topmovie in topmovies_least:
        topmovies_least_tmdbId.append(Movie.query.filter_by(movieId=topmovie.movieId).first().tmdbId)

    # 在查询wr值最高的10部电影的tmdbId，用来匹配海报文件名
    topmovies_wr_tmdbId = []
    for topmovie in topmovies_wr:
        topmovies_wr_tmdbId.append(Movie.query.filter_by(movieId=topmovie.movieId).first().tmdbId)

    return render_template('recommend/index.html', topmovies_least_tmdbId=topmovies_least_tmdbId,
                           topmovies_wr_tmdbId=topmovies_wr_tmdbId, topmovies_least=topmovies_least,
                           topmovies_wr=topmovies_wr)


@bp.route('/for-you')
def foryou():
    # 为你推荐
    # uesr_id = 1001
    recommend_movies = []

    # 检查用户是否有评分历史，如果没有，就给他推荐热门电影

    # 查询数据库中存储的用户评分
    # ratings = Rating.query.filter_by(userId=uesr_id).all()
    # 将用户评分转为dataframe格式
    # ratings_df = pd.DataFrame([rating.to_dict() for rating in ratings])
    # ratings_df = ratings_df[['userId', 'movieId', 'rating']]

    recommend_movies = str(model.get_top_n_recommendations(1034, n=10)[0])
    print(str(recommend_movies))
    return render_template('recommend/for-you.html')


@bp.route('/hot-film')
def hot_film():
    return render_template('recommend/hot-film.html')


@bp.route('/track')
def track():
    return render_template('recommend/track.html')


@bp.route('/all-film')
def all_film():
    return render_template('recommend/all-film.html') \
 \
        @ bp.route('/single')


def single():
    return render_template('recommend/single.html')
