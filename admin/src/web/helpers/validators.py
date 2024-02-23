from flask import session
from wtforms import ValidationError
from src.core import business, auth

def validate_unique_ID(form, value_ID):
    '''Valida que el socio registrado tenga identificación única en el sistema'''

    socio = auth.get_socio(value_ID.data)
    if (socio != None and socio.id != session["socio_edit"]):
        raise ValidationError('Ya existe un socio con dicha identificación.')
    
def validate_unique_email(form, email):
    '''Valida que el socio registrado tenga email único en el sistema'''

    socio = auth.get_socio_email(email.data)
    if (socio != None and socio.id != session["socio_edit"]):
        raise ValidationError('Ya existe un socio con dicho email.')
    
def validate_nombre_disciplina(self,nombre_disciplina):
    if business.disciplina_exists(nombre_disciplina.data):
        raise ValidationError('El nombre de la disciplina ingresada ya existe. Por favor elija uno distinto')