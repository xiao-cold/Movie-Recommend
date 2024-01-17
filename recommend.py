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
    return render_template('recommend/all-film.html')

@bp.route('/single')
def single():
    return render_template('recommend/single.html')

@bp.route('/single/<string:movie_title>/<string:movie_genres>')
def single1(movie_title,movie_genres=None,movie_rating=None,movie_director=None,movie_actors=None,movie_overview=None):
    return render_template('recommend/single.html',movie_title=movie_title,movie_genres=movie_genres,movie_rating=movie_rating,movie_director=movie_director,movie_actors=movie_actors,movie_overview=movie_overview)

# 将数据库中的评分数据的时间戳全部修改为当前时间
@bp.route('/update-timestamp')
def update_timestamp():
    ratings = Ratings.query.all()
    for rating in ratings:
        rating.timestamp = time.time()
    db.session.commit()
    return 'ok'
