from flask import render_template, request, Blueprint, flash, redirect, url_for, session
from sqlalchemy import asc, desc
from src.core.business.models import Disciplina
from src.core.fees import socio_moroso
from src.core import business, config, auth
from src.web.controllers.forms import AltaDisciplinaForm, AltaCategoriaForm, AltaInstructorForm, EditarDisciplinaForm
from src.web.helpers.auth import login_required
from src.web.helpers.roles import permission_required
from src.core.auth import get_all_socios
from src.web.helpers import pagination



disciplina_blueprint = Blueprint("disciplinas", __name__, url_prefix="/disciplinas")


@disciplina_blueprint.route("/",methods=["GET","POST"])
@login_required
@permission_required(perm="discipline_index")
def disciplinas_listado():
    """listado de todas las disciplinas con sus datos"""
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    disciplinas = business.list_disciplinas_categorias_instructor()
    
    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        disciplinas = disciplinas.order_by(Disciplina.nombre_disciplina.asc(), Disciplina.habilitada.desc())
    else:
        disciplinas = disciplinas.order_by(Disciplina.nombre_disciplina.desc(), Disciplina.habilitada.desc())

    pages = disciplinas.paginate(page=page, per_page=config.ELEM_PER_PAGE())
    return render_template('business/disciplinas.html',pages=pages)


@disciplina_blueprint.route("/alta", methods=["GET","POST"])
@login_required
@permission_required(perm="discipline_new")
def alta_disciplina():
    """Da de alta una disciplina si se provee nombre de la disciplina, costo, detalle de los dias,
        un instructor y una categoria"""
    form1 = AltaDisciplinaForm()
    form2 = AltaCategoriaForm()
    form3 = AltaInstructorForm()
    if(request.method == 'POST'):
        if(form1.validate_on_submit() and form2.validate_on_submit() and form3.validate_on_submit()):
            try:
                instructor = business.get_instructor(form3.nombre_instructor.data,form3.apellido_instructor.data)
                if (instructor == None):
                    instructor = business.load_instructor(nombre_instructor = form3.nombre_instructor.data, 
                                                            apellido_instructor = form3.apellido_instructor.data) 
                categoria = business.get_categoria(descripcion = form2.descripcion.data)
                if(categoria == None):
                    categoria = business.load_categoria(descripcion = form2.descripcion.data)
                    
                disciplina = business.load_disciplina(habilitada = form1.habilitada.data,
                                                        detalle = form1.detalle.data,
                                                            nombre_disciplina = form1.nombre_disciplina.data,
                                                                costo = form1.costo.data)

                business.assign_instructores(disciplina,[instructor])
                business.assign_categorias(disciplina,[categoria])
                flash(f'La disciplina {form1.nombre_disciplina.data} se creo correctamente','success')
                return redirect(url_for('disciplinas.disciplinas_listado'))
            except:
                flash(f'La disciplina no pudo ser creada','error')
                return redirect(url_for("disciplinas.alta_disciplina"))
    return render_template('business/alta_disciplinas.html',form1=form1,form2=form2,form3=form3)


@disciplina_blueprint.route("/editar/<id>", methods=["GET","POST"])
@login_required
@permission_required("discipline_update")
def editar_disciplina(id):
    """Permite editar disciplinas, modificando la informacion existente o 
                            agregando instructores o categorias a la disciplina"""
    disciplina_to_update = business.get_disciplina_by_id(id)
    categorias = business.list_categorias_from_disciplina_id(id)
    instructores = business.list_instructores_from_disciplina_id(id)

    form = EditarDisciplinaForm(obj=disciplina_to_update)
    
    if request.method == "POST":
        if(form.validate_on_submit()):
            disciplina_to_update.nombre_disciplina = form.nombre_disciplina.data
            disciplina_to_update.costo = form.costo.data
            disciplina_to_update.detalle = form.detalle.data
            disciplina_to_update.habilitada = form.habilitada.data
        try:
            business.update_disciplina(disciplina_to_update)
            message = "Disciplina {} actualizada".format(disciplina_to_update.nombre_disciplina)
            flash(message, "success")
            return redirect(url_for("disciplinas.disciplinas_listado"))
        except:
            flash("Error, intente de vuelta", "error")
            return render_template('business/editar_disciplina.html', form=form)

    return render_template('business/editar_disciplina.html', disciplina_to_update = disciplina_to_update,form=form,categorias = categorias, instructores=instructores)


@disciplina_blueprint.route("/delete/<id>", methods=["GET", "POST"])
@login_required
@permission_required(perm="discipline_destroy")
def delete_disciplina(id):
    """Elimina la disciplina seleccionada"""

    disciplina_to_delete = business.get_disciplina_by_id(id)
    try:
        business.delete_disciplina(disciplina_to_delete)
        message = "Disciplina {} eliminada".format(disciplina_to_delete.nombre_disciplina)
        flash(message,"success")
        return redirect(url_for("disciplinas.disciplinas_listado"))
    except:
        flash("Error, intente de vuelta","error")
        return redirect(url_for("disciplinas.disciplinas_listado"))


@disciplina_blueprint.route("/editar/desvincular_categoria/<id>/<idc>", methods=["GET", "POST"])
@login_required
@permission_required("discipline_update")
def desvincular_categoria(id,idc):
    """Desvincula una categoria de una disciplina quedando disponible para las disciplinas que aun la contienen"""

    disciplina = business.get_disciplina_by_id(id)
    categoria = business.get_categoria_by_id(idc)
    if(categoria and disciplina):
        try:
            business.unlink_categorias(disciplina,categoria)
            message = f"Se elimino la categoria de la disciplina {disciplina.nombre_disciplina}"
            flash(message,"success")
            return redirect(url_for("disciplinas.editar_disciplina",id=id,idc=idc))
        except:
            flash("Error, intente de vuelta","error")
            return redirect(url_for("disciplinas.editar_disciplina",id=id,idc=idc))


@disciplina_blueprint.route("/editar/desvincular_instructor/<id>/<idi>", methods=["GET", "POST"])
@login_required
@permission_required("discipline_update")
def desvincular_instructor(id,idi):
    """Desvincula un instructor de una disciplina quedando disponible para las disciplinas que aun lo contienen"""

    disciplina = business.get_disciplina_by_id(id)
    instructor = business.get_instructor_by_id(idi)
    if(disciplina and instructor):
        try:
            business.unlink_instructor(disciplina,instructor)
            message = f"Se elimino el instructor de la disciplina {disciplina.nombre_disciplina}"
            flash(message,"success")
            return redirect(url_for("disciplinas.editar_disciplina",id=id,idi=idi))
        except:
            flash("Error, intente de vuelta","error")
            return redirect(url_for("disciplinas.editar_disciplina",id=id,idi=idi))


@disciplina_blueprint.route("/editar/alta_instructor/<id>", methods=["GET", "POST"])
@login_required
@permission_required("discipline_update")
def alta_instructor(id):
    """ Permite dar de alta a un instructor en una disciplina en la edición de dsiciplinas """

    disciplina = business.get_disciplina_by_id(id)
    form = AltaInstructorForm()
    if(request.method == 'POST'):
        if(form.validate_on_submit()):
            nombre_instructor = form.nombre_instructor.data
            apellido_instructor = form.apellido_instructor.data
            instructor = business.get_instructor(nombre_instructor,apellido_instructor)
            if (instructor == None):
                    instructor = business.load_instructor(nombre_instructor = nombre_instructor, 
                                                            apellido_instructor = apellido_instructor)
            try:
                business.assign_instructores(disciplina,[instructor])
                flash(f'El instructor {nombre_instructor}  {apellido_instructor }se asoció correctamente a {disciplina.nombre_disciplina}','success')
                return redirect(url_for("disciplinas.editar_disciplina",id=id))
            except:
                flash("Error, intente de vuelta","error")
                return render_template('business/alta_instructor.html',form=form,id=id)
    return render_template('business/alta_instructor.html',form=form, id=id)


@disciplina_blueprint.route("/editar/alta_categoria/<id>", methods=["GET", "POST"])
@login_required
@permission_required("discipline_update")
def alta_categoria(id):
    """ Permite dar de alta a una categoria en una disciplina en la edición de disciplinas"""

    disciplina = business.get_disciplina_by_id(id)
    form = AltaCategoriaForm()
    if(request.method == 'POST'):
        if(form.validate_on_submit()):
            descripcion = form.descripcion.data
            categoria = business.get_categoria(descripcion)
            if (categoria == None):
                    categoria = business.load_categoria(descripcion=descripcion)
            try:
                business.assign_categorias(disciplina,[categoria])
                flash(f'La categoria {descripcion} se asoció correctamente a {disciplina.nombre_disciplina}','success')
                return redirect(url_for("disciplinas.editar_disciplina", id=id))
            except:
                flash("Error, intente de vuelta","error")
                return render_template('business/alta_categoria.html',form=form,id=id)
    return render_template('business/alta_categoria.html',form=form, id=id)


@disciplina_blueprint.route("<id>/inscripcion_socio", methods=["GET", "POST"])
@login_required
@permission_required("discipline_update")
def inscripcion_socio(id):
    
    disciplina = business.get_disciplina_by_id(id)
    if not disciplina.habilitada:
        flash("La disciplina no se encuentra habilitada", "error")
        return redirect(url_for("disciplinas.disciplinas_listado"))

    socios = get_all_socios()
    socios = auth.get_socios_sin_disciplina(socios, id)
    exists = socios.count() > 0
    socios = auth.socios_format(socios)

    if not exists:
        flash("No existen socios cargados", "info")
        return redirect(url_for("disciplinas.disciplinas_listado"))

    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        socios = socios.order_by(asc("apellido"), desc("estado"))
    else:
        socios = socios.order_by(desc("apellido"), desc("estado"))
    pages = socios.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())
    
    return render_template('business/inscripcion_socios.html', socios=socios, pages=pages, id=id, added="inscripcion_socio")


# Search Socio
@disciplina_blueprint.route("<id>/inscripcion_socio/search", methods=["GET", "POST"])
@login_required
@permission_required(perm="socio_show")
def search(id):

    session['estado'] = request.form.get('estado')
    session['searched'] = request.form.get('searched')

    return redirect(url_for('disciplinas.search_results', id=id))


@disciplina_blueprint.get("<id>/inscripcion_socio/search_results")
@login_required
@permission_required(perm="socio_show")
def search_results(id):
    '''Muestra resultados de búsqueda del listado de socios'''


    searched = session['searched']
    estado = session['estado']
    if not searched and estado == 'todos':
        flash("Ingrese o seleccione un criterio para realizar una búsqueda", "info")
        return redirect(url_for("disciplinas.inscripcion_socio", id=id))

    socios = auth.get_all_socios(estado, searched)
    socios = auth.get_socios_sin_disciplina(socios, id)

    if(socios.count() == 0):
        flash("No se ha encontrado ningún socio con el criterio ingresado", "error")
        return redirect(url_for('disciplinas.inscripcion_socio', id=id))

    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        socios = socios.order_by(asc("apellido"), desc("estado"))
    else:
        socios = socios.order_by(desc("apellido"), desc("estado"))
    pages = socios.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())

    return render_template("business/search.html", pages=pages, s=estado, id=id, n=searched, added="search_results")


@disciplina_blueprint.route("/inscripcion_socio/confirmar/<id>/<ids>", methods=["GET", "POST"])
@login_required
@permission_required("discipline_update")
def confirmar_inscripcion(id,ids):
    ''' Asigna una disciplina a un socio si este no registra deuda previa al mes actual y si la disciplina 
        encuentra habilitada'''

    id = str(id)
    id = [x for x in id  if x.isdigit() ] #limpia cadena recibida en id
    id = int(id.pop())

    disciplina = business.get_disciplina_by_id(id)
    if not disciplina.habilitada:
        flash(f"La disciplina '{disciplina.nombre_disciplina}' se encuentra deshabilitada", "error")
        return redirect(url_for("disciplinas.disciplinas_listado"))

    socio = auth.get_socio_id(ids)

    if not socio_moroso(ids):
        auth.assign_disciplinas(socio,[disciplina])
        flash(f"El socio {socio.nombre} {socio.apellido} fue asignado correctamente a {disciplina.nombre_disciplina}", "success")
        return render_template('business/confirmar_inscripcion.html', socio=socio,disciplina=disciplina,id=id,ids=ids)
    else:
        
        flash(f"El socio {socio.nombre} {socio.apellido} con número {socio.id} es moroso", "error")
        return redirect(url_for('disciplinas.inscripcion_socio',id=id))


            