from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask import jsonify
from src.core.fees import pagar_cuota_mas_antigua
from src.core.auth.schemas import SocioSchema
from src.core.auth import get_socio_id
from src.core.fees.schemas import CuotaSchema
from src.core.fees import get_cuotas_socios
from src.core.auth import get_disciplinas_from_socio
from src.core.business.schemas import DisciplinaSchema
from src.core.fees import socio_moroso
import json


api_socio_blueprint = Blueprint("api_socio", __name__, url_prefix="/api/me")


@api_socio_blueprint.get("/disciplinas/<ids>")
@jwt_required()
def disciplinas(ids):
    ''' API REST devuelve listado de disciplinas de un socio cuyo id se recibe como parametro'''
    
    disciplinas = get_disciplinas_from_socio(ids)
    disciplinas_schema = DisciplinaSchema()
    listado = []
    for item in disciplinas:
        for disciplina in item.disciplinas:
            dump = disciplinas_schema.dump(disciplina)
            dump['costo'] = '$' + str(dump['costo'])
            listado.append(dump)

    return listado, 200

@api_socio_blueprint.get("/payments/<ids>") 
@jwt_required()
def pagos(ids):
    ''' API REST devuelve listado de pagos de un socio cuyo id se recibe como parametro'''

    socio = get_socio_id(ids)
    cuota_schema = CuotaSchema()
    cuotas = get_cuotas_socios(key=socio.id, id=True)
    listado=[]
    for cuota in cuotas:
        dump = cuota_schema.dump(cuota)
        dump['monto'] = '$' + str(dump['monto'])
        dump['detalle'] = json.loads(cuota.detalle)
        listado.append(dump)
    return listado, 200

@api_socio_blueprint.post("/payments")
@jwt_required()
def pagar():
    '''API REST para realizar pago de la cuota más antigua sin pagar de un socio.'''

    res = pagar_cuota_mas_antigua(request.form.get('id'), request.files)
    if res:
        response = jsonify()
        return response, 200
    else:
        response = jsonify(message="Missing arguments")
        return response, 419


@api_socio_blueprint.get("/license/<ids>")
@jwt_required()
def estado_socio(ids):
    '''API REST obtiene el socio y el estado de cuenta de un socio cuyo id se recibe como parametro'''

    socio = get_socio_id(ids)
    moroso = socio_moroso(ids)
    socio_schema = SocioSchema()
    info = {
        "estado": "OK" if (not moroso and socio.estado_act_block) else "MOROSO" if (moroso) else "BLOQUEADO",
        "descripcion" : "Socio sin deudas ni sanción" if (not moroso and socio.estado_act_block)\
                            else "Socio con deuda" if (moroso) else "Socio con sanción",
        "socio" : socio_schema.dump(socio)
    }

    return info, 200