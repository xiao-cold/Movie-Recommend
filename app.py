import os

from flask import Flask
from algorithm.svd import RecModel
from database import db

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "530712"
DATABASE = "db_movies"


# create and configure the app
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    # 绑定app和db
    db.init_app(app)
    with app.app_context():
        # 在应用上下文内实例化 RecModel
        app.model = RecModel(model_path='./algorithm/model/svd_model_test.joblib', db=db)

    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
    import auth
    app.register_blueprint(auth.bp)
    import recommend
    app.register_blueprint(recommend.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
