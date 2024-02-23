from src.core.fees import socio_moroso
from src.core.auth import get_socio_id
from src.core.image import get_image
import json

def socio_format(socio):  
    '''Le da formato a la información de los socios para mostrarlas en pantalla de una forma legible al usuario.'''

    estado = socio_moroso(socio.id)

    disciplinas = [disciplina.nombre_disciplina for disciplina in socio.disciplinas]
    
    dict_socio = {
        "id": socio.id,
        "nombre": f"{socio.nombre} {socio.apellido}",
        "tipo_identificacion": socio.tipo_identificacion,
        "identificacion": socio.identificacion,
        "email": socio.email,
        "genero": socio.genero,
        "telefono": socio.telefono,
        "domicilio": socio.domicilio,
        "fecha_alta": socio.fecha_alta,
        "disciplinas": disciplinas,
        "estado": estado,
        "image" : socio.image,
    }
    return dict_socio

def generar_informacion(cuota):
    '''Retorna la información de una cuota en un diccionario.'''
    
    socio = get_socio_id(cuota.socio_id)

    detalle = json.loads(cuota.detalle)

    fecha_pago = "" if cuota.fecha_pago is None else cuota.fecha_pago.strftime("%d-%m-%Y")

    informacion = {
        "id" : cuota.id,
        "nombre" : socio.nombre + " " + socio.apellido,
        "socio" : cuota.socio_id,
        "monto" : cuota.monto,
        "fecha_creacion" : cuota.created_at.strftime("%d-%m-%Y"),
        "fecha_mod" : cuota.updated_at.strftime("%d-%m-%Y"),
        "fecha_pago" : fecha_pago,
        "estado" : cuota.estado,
        "detalle" : detalle,
    }
    
    return informacion

def generar_info_carnet(socio_id):
    socio = get_socio_id(socio_id)
    socio = socio_format(socio)

    informacion = {
        "id" : socio['id'],
        "nombre" : socio['nombre'],
        "tipo_identificacion" : socio['tipo_identificacion'],
        "identificacion" : socio['identificacion'],
        "fecha_alta" : socio['fecha_alta'].strftime("%d/%m/%Y"),
        "estado" : socio['estado'],
        "image_id" : socio['image'].id,
    }

    return informacion