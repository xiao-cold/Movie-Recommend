import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "db_movies"

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
db = SQLAlchemy(app)
# db.init_app(app)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# from flaskr import db
# db.init_app(app)
from . import auth

app.register_blueprint(auth.bp)
# from . import auth
# app.register_blueprint(db.bp)
from . import recommend

app.register_blueprint(recommend.bp)
