from flask import render_template


def unauthorized(e):
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": "Debe iniciar sesión para acceder al recurso", 
    }
    return render_template("error.html", **kwargs), 401


def forbidden(e):
    kwargs = {
        "error_name": "403 Forbidden",
        "error_description": "No tiene los permisos necesarios para acceder al recurso", 
    }
    return render_template("error.html", **kwargs), 403

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def internal_server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Error interno del servidor",
    }
    return render_template("error.html", **kwargs), 500
