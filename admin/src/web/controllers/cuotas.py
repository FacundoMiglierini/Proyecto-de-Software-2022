import platform
from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from datetime import datetime
from src.core.auth.models import Socio
from src.core.fees.models import Cuota
from src.web.helpers.roles import permission_required
from src.web.helpers.auth import login_required
from src.web.helpers import pagination
from src.web.helpers.formatters import generar_informacion
from src.core import auth
from src.core import fees
from src.core import config
from src.web.controllers import exporter

cuotas_blueprint = Blueprint("pagos", __name__, url_prefix="/pagos")

@cuotas_blueprint.route("/", methods=["GET", "POST"])
@login_required
@permission_required(perm="payments_index")
def searcher():
    '''Renderer de barra de búsqueda de socios para mostrar sus cuotas.
    Se muestra un listado de todas las cuotas del mes.'''
        
    cuotas = fees.get_cuotas_mes(datetime.now())
    cuotas = fees.cuotas_format(cuotas)
    
    exists = True if cuotas.count() > 0 else False

    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        cuotas = cuotas.order_by(Socio.apellido.asc(), Cuota.estado.desc())
    else:
        cuotas = cuotas.order_by(Socio.apellido.desc(), Cuota.estado.desc())
        
    pages = cuotas.paginate(page=pagination.pagination(), per_page=config.get_configuration().cant_elem)
    
    pendings = True if fees.exist_pendings() else False

    return render_template("cuotas/searcher.html", cuotas=cuotas, exists=exists, pages=pages, pendings=pendings)

@cuotas_blueprint.route("/search", methods=["GET", "POST"])
@login_required
@permission_required(perm="payments_show")
def search():
    '''Guarda el input ingresado en la búsqueda de socios para listar sus cuotas 
    y redirecciona a la función que muestra los resultados.'''    

    session["input"] = request.form["input"] 
    return redirect(url_for("pagos.search_results")) 

@cuotas_blueprint.get("/search_results") 
@login_required
@permission_required(perm="payments_show")
def search_results():
    '''Listado de todos los pagos del/los socio/s indicado/s'''
    
    input = session.get("input")
    amount_socios, type_id= auth.get_socios_by_lastname_or_id(input)
        
    if amount_socios == 0:
        flash("No existe un socio con dicho número de socio o apellido", "error")
        return redirect(url_for("pagos.searcher"))

    cuotas = fees.get_cuotas_socios(input, type_id) 
    if cuotas.count() == 0:
        flash("El socio indicado aún no dispone de cuotas pagas ni impagas", "info")
        return redirect(url_for("pagos.searcher"))
    
    order = True if config.get_configuration().criterio == "asc" else False
    
    if order:
        cuotas = cuotas.order_by(Socio.apellido.asc(), Cuota.estado.desc())
    else:
        cuotas = cuotas.order_by(Socio.apellido.desc(), Cuota.estado.desc())
    pages = cuotas.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())

    return render_template("cuotas/index.html", cuotas=cuotas, pages=pages, exists=True)

@cuotas_blueprint.get("/pendings")
@login_required
@permission_required(perm="payments_index")
def index_pendings():
    '''Listado de todas las cuotas pendientes'''

    cuotas = fees.get_cuotas_pendientes()
    if cuotas.count() == 0:
        flash("No existen cuentas pendientes", "success")
        return redirect(url_for("pagos.searcher"))

    order = True if config.get_configuration().criterio == "asc" else False

    if order:
        cuotas = cuotas.order_by(Cuota.id.asc())
    else:
        cuotas = cuotas.order_by(Cuota.id.desc())
    pages = cuotas.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())
    
    return render_template("cuotas/index_pendings.html", cuotas=cuotas, pages=pages, exists=cuotas.count() > 0)

@cuotas_blueprint.get("/show_payment/<id>")
@login_required
@permission_required(perm="payments_import")
def show_pending_payment(id):
    '''Muestra foto de comprobante de cuota pendiente'''
    
    cuota = fees.cuota(id)
    file = cuota.comprobante.split("\\")[-1]
    if platform.system() == 'Windows':
        path = '../../../../public/images/comprobantes/' + file
    # Linux or MacOs
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        path = '../../../../' + file
    return render_template("cuotas/pending_payment.html", path=path, cuota=cuota)

@cuotas_blueprint.get("/show_payment/<id_cuota>/<selected>")
@login_required
@permission_required(perm="payments_import")
def accept_or_deny_payment(id_cuota, selected):
    if selected == 'Accept':
        return redirect(url_for("pagos.pagar_cuota", id_cuota=id_cuota))
    else:
        cuota = fees.cuota(id_cuota)
        cuota.estado = "Impaga"
        fees.update_cuota(cuota)
        flash("Cuota RECHAZADA con éxito", "success")
        return redirect(url_for('pagos.searcher'))

@cuotas_blueprint.get("/socio/<id>")
@login_required
@permission_required(perm="payments_index")
def cuotas_socio(id):
    '''Listado de todos los pagos del socio indicado.'''

    cuotas = fees.get_cuotas_socios(id, True)
    if cuotas.count() == 0:
        flash("El socio indicado aún no dispone de cuotas pagas ni impagas", "success")
        return redirect(url_for("socios.index_socios"))
        
    order = True if config.get_configuration().criterio == "asc" else False
    if order:
        cuotas = cuotas.order_by(Socio.apellido.asc(), Cuota.estado.desc())
    else:
        cuotas = cuotas.order_by(Socio.apellido.desc(), Cuota.estado.desc())
    pages = cuotas.paginate(page=pagination.pagination(), per_page=config.ELEM_PER_PAGE())

    return render_template("cuotas/index.html", cuotas=cuotas, pages=pages, exists=True)

@cuotas_blueprint.get("/generate_cuotas")
@login_required
@permission_required(perm="payments_import")
def create_cuotas():
    '''Genera las cuotas del mes para todos los socios que aún no dispongan de una cuota en el mes actual'''

    counter = fees.generate_cuotas()
    if counter == 0:
        flash("No se han generado cuotas porque no existen socios cargados o porque todos los socios activos ya tienen una cuota para este mes", "success")
    elif counter == 1:
        flash("Se ha generado una cuota", "success")
    else:
        flash(f"Se han generado {counter} cuotas", "success")

    return redirect(url_for("pagos.searcher"))

@cuotas_blueprint.get("/pagar_cuota/<id_cuota>")
@login_required
@permission_required(perm="payments_import")
def pagar_cuota(id_cuota):
    '''Pago de la cuota indicada por parámetro'''

    res = fees.pagar_cuota(fees.cuota(id_cuota))
    if res is False:
        flash(f"La cuota #{id_cuota} ya se encuentra pagada", "error")
        return redirect(url_for("pagos.searcher"))

    flash(f"Se ha realizado el pago de la cuota #{id_cuota} con éxito", "success")
    return redirect(url_for("pagos.show_info_cuota", id_cuota=id_cuota))

@cuotas_blueprint.get("cuota/<id_cuota>")
@login_required
@permission_required(perm="payments_show")
def show_info_cuota(id_cuota):
    '''Muestra en pantalla toda la información de la cuota que tiene el id recibido
    como parámetro.
    Si la cuota está pagada, se muestra en formato de recibo de pago.'''

    cuota = fees.cuota(id_cuota)
    
    informacion = generar_informacion(cuota)
    if cuota.estado == "Pagada":
        session['cuota_info'] = informacion
        informacion["recibo_txt"] = config.get_configuration().recibo_txt
        return render_template("cuotas/show_comprobante.html", comprobante=informacion)
    elif cuota.estado == "Pendiente":
        return redirect(url_for("pagos.show_pending_payment", id=cuota.id))
    else:
        return render_template("cuotas/informacion.html", informacion=informacion)
    
@cuotas_blueprint.get("/download")
@login_required
@permission_required(perm="payments_show")
def download():
    informacion = session['cuota_info']
    return exporter.cuota_pdf_report(informacion)