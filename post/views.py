import json
from datetime import datetime

from flask import Blueprint, request

from app import r
from utils import get_last_value

blueprint = Blueprint('post', __name__)


@blueprint.route('/api/posts', methods=['GET'])
def get_posts():
    return json.loads(r.hgetall('post'))


@blueprint.route('/api/posts', methods=['POST'])
def make_post(title, content, author):
    key = 'post'
    last_post = get_last_value(key)
    body = dict()
    body['id'] = last_post['id'] + 1
    body['title'] = title
    body['content'] = content
    body['author'] = author
    body['created_at'] = datetime.now()
    body['updated_at'] = datetime.now()
    return r.set(key, json.dumps(body))


@blueprint.route('/api/posts/<slug>', methods=['GET'])
def get_post(slug):
