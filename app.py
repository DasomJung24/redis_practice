import redis
from flask import Flask
from flask_cors import CORS

from exceptions import InvalidUsage


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': '*'}})
    # register_redis(app)
    register_errorhandlers(app)
    return app


try:
    r = redis.Redis(host='127.0.0.1', port='6379', db='0', decode_responses=True)
    # return r
except redis.RedisError as exception:
    raise exception


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)