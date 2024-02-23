from flask import session
from flask import abort
from functools import wraps

def is_authenticated(session):
    return session.get("username") != None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function