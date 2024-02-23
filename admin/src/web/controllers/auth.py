from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from src.core import auth
from src.web.helpers.auth import login_required

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.post("/authenticate") 
def authenticate():
    '''Autentica los datos de sesión ingresados.
    En caso de ser incorrectos, se retorna un mensaje de error.
    En caso de ser correctos, se loguea al usuario y se muestra un mensaje de error.'''

    user = auth.find_user_by_username_and_pass(request.form["username"], request.form["password"])
    if not user:
        flash("Username o clave incorrecta.", "error")
        return redirect(url_for("landing"))

    if not user.estado:
        flash("Cuenta bloqueada", "error")
        return redirect(url_for("landing"))

    session["username"] = user.username
    flash("La sesión se inició correctamente.", "success")
    
    return redirect(url_for("user.index_users"))


@auth_blueprint.get("/logout")
@login_required
def logout():
    '''Desautentica al usuario.'''

    del session["username"]
    session.clear()

    return redirect(url_for("landing"))
