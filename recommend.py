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
    #
    context = str(model.get_top_n_recommendations(100234, n=10)[0])
    print(str(context))
    # 查询数据库
    topmovies = Top_Movies.query.all()
    # 筛选year最近的10部电影
    topmovies_least = sorted(topmovies, key=lambda x: x.year, reverse=True)[:10]
    # 筛选wr值最高的10部电影
    topmovies_wr = sorted(topmovies, key=lambda x: x.wr, reverse=True)[:10]

    movies = Movie.query.filter_by(movieId=5796)
    context = topmovies
    # print a list
    # for i in topmovies:
    #     # print(i.movieId, i.title, i.year, i.wr)

    return render_template('recommend/index.html', context=movies)

@bp.route('/new-film')
def new_film():
    return render_template('recommend/new-film.html')


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
 \
@bp.route('/single')
def single():
    return render_template('recommend/single.html')
