from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


POST_NOT_FOUND = template(['Post not found'], code=404)
UNKNOWN_ERROR = template([], code=500)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def post_not_found(cls):
        return cls(**POST_NOT_FOUND)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)