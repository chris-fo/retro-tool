import logging

from flask import jsonify
from flask_api import status
from flask_restful import Resource, abort, reqparse
from db.db import get_db


class User(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=dict)

    def get(self, user_id):
        db = get_db()
        logging.warning(f"User ID: {user_id}")
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id, )).fetchone()
        db.close()
        if user is None:
            abort(status.HTTP_404_NOT_FOUND, message=f"No user with ID {user_id} found!")
        return jsonify(user), status.HTTP_200_OK

    def post(self):
        db = get_db()
        args = self.parser.parse_args()
        user = args["user"]
        db.execute("INSERT INTO user(username, password) VALUES(:username, :password)", user)
        db.close()
        return f"Created user {user['username']}", status.HTTP_201_CREATED

