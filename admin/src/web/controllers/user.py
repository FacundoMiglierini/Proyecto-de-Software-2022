from flask import render_template, Blueprint, flash, request, redirect, url_for, session
from src.core.auth.models import User
from src.web.helpers import pagination
from src.core import auth, roles, config
from src.web.controllers.forms import RegisterUserByAdminForm, EditUserByAdminForm
from src.web.helpers.auth import login_required
from src.web.helpers.choices_loader import load_roles, load_user_estados
from src.web.helpers.roles import permission_required

user_blueprint = Blueprint("user", __name__, url_prefix="/user")

# List Users
@user_blueprint.route("/index", methods=["GET", "POST"])
@login_required
@permission_required(perm="user_index")
def index_users():
    '''Manejador de vista que muestra un listado con todos los usuarios, permitiendo realizar
    búsquedas por distintos criterios'''
        
    users = auth.list_users()
    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        users = users.order_by(User.apellido.asc(), User.estado.desc())
    else:
        users = users.order_by(User.apellido.desc(), User.estado.desc())
        
    pages = users.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())

    return render_template("user/base_listado_usuarios.html", pages=pages, added="index")


# Create Users
@user_blueprint.route("/create", methods=["GET", "POST"])
@login_required
@permission_required(perm="user_new")
def create_user():
    form = RegisterUserByAdminForm()
    form.roles.choices = load_roles()
    if form.validate_on_submit(): 
        user_to_create = auth.get_exact_user(username=form.username.data, email=form.email.data)
        if(user_to_create == None):
            auth.load_user(username = form.username.data,
                            email = form.email.data,
                            nombre = form.name.data.capitalize(),
                            apellido = form.lastname.data.capitalize(),
                            password = form.password.data)
            flash("Usuario agregado", "success")
            return redirect(url_for("user.index_users"))
        else:
            if(user_to_create.email == form.email.data):
                message = "El mail {} ya existe".format(user_to_create.email)
                flash(message, "error")
            elif(user_to_create.username == form.username.data):
                message = "El usuario {} ya existe".format(user_to_create.username)
                flash(message, "error")
            return redirect(url_for("user.create_user"))
    return render_template("user/alta_usuarios.html", form=form)


# Update Users
@user_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@permission_required(perm="user_update")
def edit_user(id):
    user_to_update = auth.get_user_id(id)
    if id == 1 or user_to_update.username == session["username"]:
        flash("No se puede editar el usuario seleccionado", "error")
        return redirect(url_for("user.index_users"))
    form = EditUserByAdminForm(obj=user_to_update)
    form.estado.choices = load_user_estados()
    form.roles.choices = load_roles()
    form.password = user_to_update.password
    if form.validate_on_submit():
        # User new data
        user_to_update.nombre = request.form['name'].capitalize()
        user_to_update.apellido = request.form['lastname'].capitalize()
        user_to_update.username = request.form['username']
        user_to_update.email = request.form['email']
        user_to_update.estado = False if request.form['estado'] == 'False' else True
        if(form.roles.data is not None):
            added = []
            for nombre_rol in form.roles.data:
                next = roles.get_rol_by_name(nombre_rol)
                added.append(next)
            roles.assign_roles(user_to_update, added)
        
        # Update user in db
        try:
            auth.update_user(user_to_update)
            message = "Usuario {} actualizado".format(user_to_update.username)
            flash(message, "success")
            return redirect(url_for("user.index_users"))
        except:
            flash("Error, intente de vuelta", "error")
            return render_template("user/editar_usuarios.html", form=form, user_to_update=user_to_update)
    return render_template("user/editar_usuarios.html", form=form, user_to_update=user_to_update)

# Delete Users
@user_blueprint.route("/delete/<int:id>")
@login_required
@permission_required("user_destroy")
def delete_user(id):
    user_to_delete = auth.get_user_id(id)
    try:
        auth.delete_user(id)
        message = "Usuario {} eliminado".format(user_to_delete.username)
        flash(message, "success")
        return redirect(url_for("user.index_users"))
    except:
        flash("Error, intente de vuelta", "error")
        return redirect(url_for("user.index_users"))


# Search Users Function
@user_blueprint.route('/search', methods=["GET", "POST"])
@login_required
@permission_required(perm="user_show")
def search():
    params = request.form
    session['estado'] = params.get('estado')
    session['searched'] = params.get('searched')
    
    return redirect(url_for('user.search_results'))

@user_blueprint.get("/search_results")
@login_required
@permission_required(perm="user_show")
def search_results():
    '''Filtra los usuarios según los criterios ingresados'''
    users = auth.list_users()

    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        users = users.order_by(User.apellido.asc(), User.estado.desc())
    else:
        users = users.order_by(User.apellido.desc(), User.estado.desc())

    searched = session['searched']
    estado = session['estado']
    if not searched and estado == 'todos':
        flash("Ingrese o seleccione un criterio para realizar una búsqueda", "info")
        return redirect(url_for("user.index_users"))
    
    if searched:
        users = auth.get_by_search_string(users, searched)
    
    if estado != 'todos':
        if estado == 'True':
            users = auth.get_by_estado(users, True)
        else:
            users = auth.get_by_estado(users, False)
    
    if(users.count() == 0):
        flash("No se ha encontrado ningún usuario con el criterio ingresado", "error")
        return redirect(url_for('user.index_users'))
    
    pages = users.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())
    return render_template("user/buscar_usuario.html", pages=pages, s=estado, n=searched, added="search_results")
