from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint('recommend', __name__)



@bp.route('/')
def recommend():
    return redirect(url_for('recommend.index'))

@bp.route('/index')
def index():
    return render_template('recommend/index.html')

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



