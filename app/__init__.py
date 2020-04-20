import os
from flask import Flask

from os.path import join, dirname
from flask import (
    render_template
)

from werkzeug.exceptions import HTTPException

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
        MODEL_FOLDER=os.path.join(app.instance_path, 'models'),
        TIMESTAMP_COLUMN_NAME="Timestamp",
        VALUE_COLUMN_NAME="Value",
        N_INPUT=24,
        N_FEATURES=1,
        DATE_TIME_FROMAT="%Y-%m-%d %H:%M:%S",
        LSTM="lstm",
        ARIMA="arima",
        PROPHET="prophet",
        ITEM_PER_PAGE=5,
        SERVER_HOST=os.getenv('SERVER_HOST'),
        SERVER_PORT=os.getenv('SERVER_PORT')
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import eda
    app.register_blueprint(eda.bp)

    return app
