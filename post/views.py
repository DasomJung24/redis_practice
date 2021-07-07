import json
from datetime import datetime
from flask import Blueprint, request
from redis_conn import r


from exceptions import InvalidUsage
from utils import make_redis_id, get_redis_json_data, json_default, get_redis_json_data_list

blueprint = Blueprint('posts', __name__)


@blueprint.route('/api/posts', methods=['GET'])
def get_posts():
    posts = get_redis_json_data_list('post:*')
    return {'data': posts}


@blueprint.route('/api/posts', methods=['POST'])
def make_post():
    data = request.get_json()
    body = {
        'id': make_redis_id('post:*'),
        'title': data['title'],
        'content': data['content'],
        'author': data['author'],
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    key = f"post:{body['id']}"
    r.set(key, json.dumps(body, default=json_default))
    return json.dumps(body, default=json_default), 201


@blueprint.route('/api/posts/<slug>', methods=['GET'])
def get_post(slug):
    post = get_redis_json_data(f'post:{slug}')
    if not post:
        raise InvalidUsage.post_not_found()
    return post


@blueprint.route('/api/posts/<slug>', methods=['PUT'])
def update_post(slug):
    data = request.get_json()
    post = get_redis_json_data(f'post:{slug}')
    body = {
        'id': post['id'],
        'title': data['title'],
        'content': data['content'],
        'author': post['author'],
        'created_at': post['created_at'],
        'updated_at': datetime.now()
    }
    key = f"post:{post['id']}"
    r.set(key, json.dumps(body, default=json_default))
    return json.dumps(body, default=json_default)


@blueprint.route('/api/posts/<slug>', methods=['DELETE'])
def delete_post(slug):
    post = get_redis_json_data(f'post:{slug}')
    if not post:
        raise InvalidUsage.post_not_found()
    r.delete(f'post:{slug}')
    return '', 204
