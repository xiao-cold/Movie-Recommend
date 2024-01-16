from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from algorithm.svd import RecModel
from mydb import Movie, Top_Movies

bp = Blueprint('recommend', __name__)


@bp.route('/')
def recommend():
    return redirect(url_for('recommend.index'))


@bp.route('/index')
def index():
    model = RecModel()
    context = str(model.get_top_n_recommendations(34, n=10)[0])

    # 查询数据库
    topmovies = Top_Movies.query.all()
    # 筛选year最近的10部电影
    topmovies_least = sorted(topmovies, key=lambda x: x.year, reverse=True)[:10]
    # 筛选wr值最高的10部电影
    topmovies_wr = sorted(topmovies, key=lambda x: x.wr, reverse=True)[:10]

    context = topmovies
    print(context.head())

    return render_template('recommend/index.html', context=context)

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
    return render_template('recommend/all-film.html')



