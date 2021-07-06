from app import r


def get_last_value(key):
    posts = r.hgetall('post')
    return posts.pop()