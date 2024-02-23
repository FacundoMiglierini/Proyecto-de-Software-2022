from flask import render_template, Blueprint, flash, redirect, url_for, session, request
from src.web.helpers.choices_loader import load_roles_without_admin
from src.core import auth, roles
from src.web.controllers.forms import EditProfileByAdminForm
from src.core import config
from src.web.helpers.choices_loader import load_tabla_pagos, load_criterio
from src.web.helpers.auth import login_required
from src.web.helpers.roles import permission_required
from src.web.controllers.forms import ConfigForm

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@admin_blueprint.route("/config", methods=["GET", "POST"])
@login_required
@permission_required(perm="config")
def configuration():
    act_config = config.get_configuration()
    form = ConfigForm(criterio=act_config.criterio)
    form.cant.default = act_config.cant_elem
    form.cant_pagos_permitidos.default = act_config.cant_pagos_permitidos
    form.criterio.choices = load_criterio()
    form.pagos.choices = load_tabla_pagos()
    if form.validate_on_submit():
        act_config.cant_elem = form.cant.data
        act_config.criterio = form.criterio.data
        act_config.pagos = form.pagos.data
        act_config.cant_pagos_permitidos = form.cant_pagos_permitidos.data
        act_config.email = form.email.data
        act_config.phone = form.phone.data
        act_config.recibo_txt = form.recibo_txt.data if form.recibo_txt.data is not None else ""
        act_config.cuota_base = form.cuota_base.data
        act_config.recargo = form.recargo.data

        config.update_configuration(act_config)
        flash("Configuración actualizada", "success")
        return redirect(url_for("user.index_users"))
    return render_template("admin/config.html", form=form, config=act_config)

@admin_blueprint.route("/profile", methods=["GET", "POST"])
@login_required
@permission_required(perm="profile")
def profile():
    admin_username = session.get("username")
    admin_edit = auth.get_user_by_username(admin_username)
    form = EditProfileByAdminForm(obj=admin_edit)
    
    # Datos que NO se pueden modificar
    form.roles.choices = load_roles_without_admin()

    # Datos que sí se pueden modificar
    if form.validate_on_submit():
        admin_edit.nombre = (form.name.data).capitalize()
        admin_edit.apellido = request.form['lastname'].capitalize()
        admin_edit.email = request.form['email']
        if(form.roles.data is not None):
            added = []
            for nombre_rol in form.roles.data:
                next = roles.get_rol_by_name(nombre_rol)
                added.append(next)
            roles.assign_roles(admin_edit, added)
        
        # Update user in db
        try:
            auth.update_user(admin_edit)
            message = "Usuario {} actualizado".format(admin_edit.username)
            flash(message, "success")
            return render_template("admin/profile.html", form=form, admin=admin_edit)
        except:
            flash("Error, intente de vuelta", "error")
            return render_template("admin/profile.html", form=form, admin=admin_edit)

    return render_template("admin/profile.html", form=form, admin=admin_edit)