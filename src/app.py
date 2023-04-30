import os

from flask import Flask
from flask_restful import Api, reqparse

from db.db import init_db
from resources.user import User


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'retro-tool.sqlite'),
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

    init_db(app)
    api = Api(app)

    user_routes = [
        "/user",
        "/user/<user_id>"
    ]
    api.add_resource(User, *user_routes)

    return app

