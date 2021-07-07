import json
from datetime import datetime

from redis_conn import r


def make_redis_id(key):
    p_li = list()
    for i in r.scan_iter(match=key):
        p_li.append(int(i.split(':')[1]))

    if len(p_li) == 0:
        return 1

    return max(p_li) + 1


def redis_key_exists(key):
    if r.exists(key):
        return True
    return False


def get_redis_json_data_list(key):
    p_li = list()
    for i in r.scan_iter(match=key):
        p_li.append(json.loads(r.get(i)))

    return p_li


def get_redis_json_data(key):
    if r.exists(key):
        resource = r.get(key)
        return json.loads(resource)

    return False


def json_default(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError('not JSON serializable')
