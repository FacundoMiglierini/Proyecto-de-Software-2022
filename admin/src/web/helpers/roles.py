from functools import wraps
from flask import session
from flask import abort
from src.core.roles import role_has_permission
from src.core.auth import get_user_by_username

def user_has_permission(permission):
    '''Chequea si el user logueado tiene un permiso asignado'''

    user = get_user_by_username(session.get("username"))

    if user == None:
        return False
    else:
        for role in user.roles:
            if (role_has_permission(role, permission)):
                return True
        return False

def permission_required(perm, *args, **kwargs):
    '''Chequea si el user logueado tiene un permiso asignado'''

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if (not user_has_permission(perm)):
                return abort(403)
            return f(*args, **kwargs)

        return decorated_function
    return decorator
    