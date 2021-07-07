from flask import Flask
from flask_cors import CORS

import post
from exceptions import InvalidUsage


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': '*'}})
    register_errorhandlers(app)
    register_blueprints(app)
    return app


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_blueprints(app):
    app.register_blueprint(post.views.blueprint, prefix='/posts')