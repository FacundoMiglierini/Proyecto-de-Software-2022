from sqlalchemy.sql import extract
from src.core.database import db
from src.core.fees.models import Cuota
from src.core.auth.models import Socio
from src.core import auth, config
from src.web.helpers.adaptators import upload_file
from datetime import datetime
import json

def list_cuotas():
    return Cuota.query.order_by(Cuota.fecha_vencimiento.asc()).all()

def load_cuota(**kwargs):
    cuota = Cuota(**kwargs)
    db.session.add(cuota)
    db.session.commit()

    return cuota

def vencida(cuota):
    '''Chequea si una cuota está vencida. Una cuota se vence en el mes siguiente al que fue creada'''
    return True if (datetime.now().month - cuota.created_at.month > 0) else False
    
def calcular_monto(socio):
    '''Retorna el monto total de la cuota del mes para el socio ingresado por parámetro'''

    monto_base = config.get_configuration().cuota_base
    monto_disciplinas = sum(d.costo for d in socio.disciplinas)

    return monto_base + monto_disciplinas


def not_having_fees_this_month(socio):
    '''Retorna True si el socio no tiene una cuota generada para el mes actual.
    En caso contrario, retorna False.'''
    fees = Cuota.query.filter(Cuota.socio_id == socio.id).filter(extract('year', Cuota.created_at) == datetime.now().year).filter(extract('month', Cuota.created_at) == datetime.now().month)
    
    return fees.count() == 0

def generate_cuotas():
    '''Generar todas las cuotas del mes para todos los socios.
    Si un socio ya tiene una cuota generada para el mes actual, no se genera nuevamente.
    Se retorna la cantidad de cuotas generadas.'''
    
    counter = 0
    socios = auth.get_all_socios().filter_by(estado_act_block=True).all()
    for socio in socios:
        if (not_having_fees_this_month(socio)):
            detalle = json.dumps({
                    "base": config.get_configuration().cuota_base,
                    "disciplinas": {x.nombre_disciplina: x.costo for x in socio.disciplinas},
                    "recargo": 0,
                    },)
            load_cuota(
                monto=calcular_monto(socio),
                detalle=detalle,
                socio_id=socio.id
            )
            counter += 1

    return counter

def get_cuotas_socios(key, id=False):
    '''Retorna todas las cuotas de los socios que contengan la clave "key" indicada.
    Si id es False, se filtra por apellido.
    Si id es True, se filtra por número de socio.'''

    if not id:
        key = key.capitalize()
        socios = Socio.query.filter(Socio.apellido==key)
        cuotas = socios.join(Cuota, Socio.id == Cuota.socio_id).with_entities(Cuota.id, Cuota.monto, Cuota. estado, Cuota.created_at, Socio.nombre, Socio.apellido)
    else:
        cuotas = Cuota.query.filter_by(socio_id=key)
        cuotas = cuotas.join(Socio, Cuota.socio_id==Socio.id)\
        .filter(Socio.id == Cuota.socio_id)\
        .with_entities(Cuota.id, Cuota.monto, Cuota. estado, Cuota.created_at, Cuota.detalle, Socio.nombre, Socio.apellido)

    return cuotas

def get_cuotas_mes(fecha):
    '''Retorna todas las cuotas del mes indicado en la fecha ingresada como parámetro.'''
    
    return Cuota.query.filter(extract('year', Cuota.created_at) == fecha.year).filter(extract('month', Cuota.created_at) == fecha.month)

def get_cuotas_pendientes():
    '''Retorna todas las cuotas pendientes'''
    
    return Cuota.query.filter_by(estado="Pendiente")

def pagar_cuota(cuota):
    '''Se registra el pago de la cuota indicada por parámetro y retorna True.
    Si la cuota está vencida, se añade un recargo al monto final y se registra en el detalle.
    Si la cuota ya se encuentra pagada, retorna False'''

    if cuota.estado == "Pagada":
        return False

    detalle = json.loads(cuota.detalle)
    if vencida(cuota):
        detalle["recargo"] = config.get_configuration().recargo
        cuota.detalle = detalle
    else:
        detalle["recargo"] = 0
 
    cuota.monto = cuota.monto + detalle["recargo"] 
    cuota.fecha_pago = datetime.now()
    cuota.estado = "Pagada"
    
    update_cuota(cuota)
    
    return True

def pagar_cuota_mas_antigua(socio_id, file):
    '''Se adjunta comprobante de pago de la cuota más antigua del socio con id "socio_id", y se
    cambia el estado de dicha cuota a "Pendiente" '''
    
    cuota = cuota_mas_antigua_impaga(socio_id)
    if cuota is not None and 'file' in file:
        cuota.estado = "Pendiente"
        cuota.comprobante = upload_file(file['file'], cuota.id, socio_id)

        db.session.add(cuota)
        db.session.commit()
        
        return True
    
    return False
    
def cuota(id_cuota):
    '''Retorna la cuota asociada al id recibido por parámetro.'''

    return Cuota.query.get(id_cuota)

def socio_moroso(id):
    ''' Retorna verdadero si el socio cuenta con alguna cuota en estado "Impaga" que no sea la del mes actual'''
   
    primer_dia_mes = datetime(datetime.now().year, datetime.now().month, 1) 
    return (Cuota.query.filter_by(socio_id = id).
                            filter_by(estado='Impaga').filter(Cuota.created_at < primer_dia_mes).count() > 0)

def cuota_mas_antigua_impaga(id):
    '''Recibe una lista de cuotas y devuelve la de mayor antiguedad'''  
    
    cuota = Cuota.query.filter_by(socio_id = id).filter_by(estado='Impaga').order_by(Cuota.created_at).first()
    return cuota

def cuotas_format(cuotas):
    '''Se preparan los datos a mostrar en el listado de cuotas.'''

    cuotas = cuotas\
        .join(Socio, Cuota.socio_id==Socio.id)\
        .filter(Socio.id == Cuota.socio_id)\
        .with_entities(Cuota.id, Cuota.monto, Cuota. estado, Cuota.created_at, Socio.nombre, Socio.apellido)

    return cuotas

def exist_pendings():
    '''Retorna True si existen pagos pendientes, en caso contrario retorna False'''
    
    cuotas = Cuota.query.filter_by(estado="Pendiente")
    return cuotas.count() > 0
    
def update_cuota(cuota):
    '''Actualiza una cuota recibida por parámetro en la bd'''

    db.session.add(cuota)
    db.session.commit()