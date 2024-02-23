from flask import render_template, Blueprint, flash, request, redirect, url_for, session
from sqlalchemy import asc, desc
from src.web.helpers import pagination 
from src.core import auth
from src.core import business
from src.core import config
from src.core import image
from src.web.controllers.forms import RegisterSocioForm
from src.core.auth import assign_disciplinas, get_socio_id
from src.web.helpers.choices_loader import load_disciplinas
from src.web.helpers.choices_loader import load_genders
from src.web.helpers.choices_loader import load_type_id 
from src.web.helpers.roles import permission_required
from src.web.helpers.auth import login_required
from src.web.helpers.formatters import socio_format
from src.web.helpers.formatters import generar_info_carnet
from src.web.controllers import exporter
from src.web.helpers.adaptators import generate_qr
from src.web.helpers.adaptators import image_resize
import base64


socio_blueprint = Blueprint("socio", __name__, url_prefix="/socio")


# List Socio
@socio_blueprint.route("/index/", methods=["GET", "POST"])
@login_required
@permission_required(perm="socio_index")
def index_socios():
    '''Manejador de vista que muestra un listado con todos los socios, permitiendo realizar
    búsquedas por distintos criterios'''
    
    session['accion'] = 'Index'
    socios = auth.get_all_socios()
    exists = socios.count() > 0
    socios = auth.socios_format(socios)

    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        socios = socios.order_by(asc("apellido"), desc("estado"))
    else:
        socios = socios.order_by(desc("apellido"), desc("estado"))
    pages = socios.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())
    
    return render_template("socios/index.html", socios=socios, pages=pages, exists=exists)

# Create Socio
@socio_blueprint.route("/create", methods=["GET", "POST"])
@login_required
@permission_required(perm="socio_new")
def create_socio():
    form = RegisterSocioForm()
    form.disciplines.choices = load_disciplinas()
    form.gender.choices = load_genders()
    form.type_ID.choices = load_type_id()
    if form.validate_on_submit():
        socio = auth.load_socio(nombre=form.name.data.capitalize(),
                        apellido=form.lastname.data.capitalize(),
                        tipo_identificacion=form.type_ID.data,
                        identificacion=form.value_ID.data,
                        email=form.email.data,
                        genero=form.gender.data,
                        telefono="" if not form.phone.data else form.phone.data,
                        domicilio=form.address.data,
                        estado_act_block=True)
        if(form.disciplines.data is not None):
            added = []
            for disciplina in form.disciplines.data:
                next = business.get_disciplina(disciplina)
                added.append(next)
            assign_disciplinas(socio, added)
                
        flash("Se ha cargado el socio con éxito", "success")
        return redirect(url_for("socio.create_socio"))
        
    return render_template("socios/alta_socio.html", form=form)

# Update Socios
@socio_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@permission_required(perm="socio_update")
def edit_socio(id):
    session["socio_edit"] = id
    socio_to_update = auth.get_socio_id(id)
    form = RegisterSocioForm(obj=socio_to_update)
    form.disciplines.choices = load_disciplinas()
    form.gender.choices = load_genders()
    form.type_ID.choices = load_type_id()
    if form.validate_on_submit():
        # Socio new data
        socio_to_update.nombre = request.form['name'].capitalize()
        socio_to_update.apellido = request.form['lastname'].capitalize()
        socio_to_update.tipo_identificacion = request.form['type_ID']
        socio_to_update.identificacion = request.form['value_ID']
        socio_to_update.email = request.form['email']
        socio_to_update.genero = request.form['gender']
        socio_to_update.telefono = request.form['phone']
        socio_to_update.domicilio = request.form['address']
        nuevo_estado = request.form.get('estado')
        if nuevo_estado is not None:
            socio_to_update.estado_act_block = True if nuevo_estado == 'True' else False
        else:
            socio_to_update.estado_act_block = socio_to_update.estado_act_block
        if(form.disciplines.data is not None):
            added = []
            for disciplina in form.disciplines.data:
                next = business.get_disciplina(disciplina)
                added.append(next)
            assign_disciplinas(socio_to_update, added)
        
        del session["socio_edit"]
        # Update socio in db
        try:
            auth.update_socio(socio_to_update)
            message = "Socio {} {} actualizado".format(socio_to_update.nombre, socio_to_update.apellido)
            flash(message, "success")
            return redirect(url_for("socio.index_socios"))
        except:
            flash("Error, intente de vuelta", "error")
            return render_template("socios/editar_socio.html", form=form, socio_to_update=socio_to_update)
    del session["socio_edit"]

    return render_template("socios/editar_socio.html", form=form, socio_to_update=socio_to_update)

@socio_blueprint.get("/edit/<int:id>/switch_estado")
@login_required
@permission_required(perm="socio_switch_state")
def switch_estado(id):
    socio_to_switch = auth.get_socio_id(id)

    if socio_to_switch.estado_act_block:
        socio_to_switch.estado_act_block = False
    else:
        socio_to_switch.estado_act_block = True
    
    try:
        auth.update_socio(socio_to_switch)
        message = "Estado de socio {} {} actualizado".format(socio_to_switch.nombre, socio_to_switch.apellido)
        flash(message, "success")
        return redirect(url_for("socio.index_socios"))
    except:
        flash("Error, intente de vuelta", "error")
        return render_template("socios/index_socios.html")


# Delete Socio
@socio_blueprint.route("/delete/<int:id>")
@login_required
@permission_required(perm="socio_destroy")
def delete_socio(id):
    socio_to_delete = auth.get_socio_id(id)
    try:
        auth.delete_socio(id)
        message = "Socio {} eliminado".format(socio_to_delete.apellido)
        flash(message, "success")
        return redirect(url_for("socio.index_socios"))
    except:
        flash("Error, intente de vuelta", "error")
        return redirect(url_for("socio.index_socios"))

# Search Socio
@socio_blueprint.route("/index/search", methods=["GET", "POST"])
@login_required
@permission_required(perm="socio_show")
def search():
    session['accion'] = 'Search'
    session['estado'] = request.form.get('estado')
    session['searched'] = request.form.get('searched')

    return redirect(url_for('socio.search_results'))


@socio_blueprint.get("/index/search_results")
@login_required
@permission_required(perm="socio_show")
def search_results():
    '''Muestra los resultados de búsqueda del listado de socios'''
    
    searched = session['searched']
    estado = session['estado']
    if not searched and estado == 'todos':
        flash("Ingrese o seleccione un criterio para realizar una búsqueda", "info")
        return redirect(url_for("socio.index_socios"))

    socios = auth.get_all_socios(estado, searched)

    if(socios.count() == 0):
        flash("No se ha encontrado ningún socio con el criterio ingresado", "error")
        return redirect(url_for('socio.index_socios'))
    
    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        socios = socios.order_by(asc("apellido"), desc("estado"))
    else:
        socios = socios.order_by(desc("apellido"), desc("estado"))
    pages = socios.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())
    return render_template("socios/search.html", pages=pages, exists=True,  s=estado, n=searched, added="search_results")

# Socio information
@socio_blueprint.get("/info/<id>")
@login_required
@permission_required(perm="socio_show")
def show_info(id):
    '''Muestra la información detallada de un socio en particular.'''
    
    socio = get_socio_id(id)
    socio_format(socio)

    return render_template("socios/informacion.html", socio=socio)


# Export list
@socio_blueprint.get("/download/<opc>")
@login_required
@permission_required(perm="socio_index")
def download(opc):
    if session['accion'] == 'Index':
        socio_list = auth.get_all_socios()
    elif session['accion'] == 'Search':
        socio_list = auth.get_all_socios(session['estado'], session['searched'])
    
    if opc == 'PDF':
        return exporter.pdf_report(socio_list)
    elif opc == 'CSV':
        return exporter.csv_report(socio_list)
    

# Socio's Carnet
@socio_blueprint.route('/upload/<socio_id>', methods=['GET', 'POST'])
@login_required
@permission_required(perm="socio_show")
def upload(socio_id):

    socio = get_socio_id(socio_id)
    socio_format(socio)

    if request.method == 'POST':
        # Image
        file = request.files['file']
        if file.filename.split('.')[1] not in ['jpg', 'png']:
            flash("Sólo se permiten archivos jpg o png", "error")
            return redirect(url_for('socio.index_socios'))
        
        # Resize and encode Image
        image_64 = base64.b64encode(image_resize(file))
        mimetype = '.' + file.filename.split('.')[1]
        upload = image.load_image(filename=file.filename, data=image_64,
                                        mimetype=mimetype, socio_id=socio.id)

        message = "Carnet de socio {} creado".format(socio.id)
        flash(message, "success")
        return redirect(url_for('socio.show', socio_id=socio.id))

    return render_template('socios/upload_carnet.html', socio=socio)

@socio_blueprint.route('/<socio_id>/carnet', methods=['GET', 'POST'])
@login_required
@permission_required(perm="socio_show")
def show(socio_id):
    carnet = generar_info_carnet(socio_id)
    upload = image.get_image(carnet['image_id'])
    qr = generate_qr('https://admin-grupo19.proyecto2022.linti.unlp.edu.ar/socio/{}/carnet'.format(socio_id))
    return render_template('socios/show_carnet.html', carnet=carnet, image=upload, qr=qr)

@socio_blueprint.get('/<socio_id>/download_carnet')
@login_required
@permission_required(perm="socio_show")
def download_carnet(socio_id):
    carnet = generar_info_carnet(socio_id)
    return exporter.carnet_pdf_export(carnet)

# Crear usuario de socio
@socio_blueprint.route('/socios_user/<id>', methods=['GET', 'POST'])
@login_required
@permission_required(perm="socio_destroy")
def socios_user(id):
    socio = get_socio_id(id)
    if request.method == 'POST':
        #socio = get_socio_id(id)
        username = request.form['username']
        password = request.form['password']

        try:
            auth.update_socio_with_user(socio.id, username, password)
            message = "Usuario de socio {} {} creado".format(socio.nombre, socio.apellido)
            flash(message, "success")
            return redirect(url_for("socio.index_socios"))
        except:
            flash("Error, intente de vuelta", "error")
            return render_template("socios/alta_usuario_de_socio.html")
    return render_template("socios/alta_usuario_de_socio.html")
    