from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, PasswordField, FloatField, BooleanField, SubmitField, validators, ValidationError, IntegerField
from wtforms.validators import Regexp
from wtforms import widgets
from wtforms.widgets import TextArea
from wtforms.fields import IntegerRangeField
from src.web.helpers import validators as valid

# This code from WTForms docs, this class changes the way SelectMultipleField
# is rendered by jinja
# https://wtforms.readthedocs.io/en/3.0.x/specific_problems/
class MultiCheckboxField(SelectMultipleField):
    '''Muestra selección múltiple como checkboxes'''
    
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
# Admin
class ConfigForm(FlaskForm):
    '''Formulario de configuración'''

    cant = IntegerRangeField('Cantidad de elementos por página', [validators.NumberRange(min=1, max=100)])
    criterio = SelectField('Seleccionar criterio de ordenacion de los listados', choices=[])
    pagos = SelectField('Habilitar/Deshabilitar tabla de pagos', choices=[])
    cant_pagos_permitidos = IntegerRangeField('Cantidad de cuotas impagas permitidas', [validators.NumberRange(min=1, max=20)])
    email = StringField('Email', [validators.Email()], render_kw={"placeholder": "ejemplo@ejemplo.com"})
    phone = StringField('Teléfono', [validators.Optional(), validators.Length(min=10, max=18)], render_kw={"placeholder": "(+54) 221-000-0000"})
    recibo_txt = StringField('Encabezado de recibo de pago', render_kw={"placeholder": "Encabezado"})
    cuota_base = FloatField('Cuota mensual base $', [validators.data_required()], render_kw={"placeholder": "750.75"})
    recargo = FloatField('Recargo %',[validators.Optional()],  default=0, render_kw={"placeholder": "15"})

# Users
class RegisterUserByAdminForm(FlaskForm):
    '''Formulario de registro de usuarios'''

    name = StringField('Nombre', [validators.InputRequired(), validators.Length(min=3, max=36)])
    lastname = StringField('Apellido', [validators.InputRequired(), validators.Length(min=3, max=40)])
    username = StringField('Nombre de usuario', [validators.InputRequired(), validators.Length(min=4, max=256)])
    email = StringField('Mail', [validators.InputRequired(), validators.Email(), validators.Length(min=6, max=120)])
    password = PasswordField('Contraseña', [validators.InputRequired(), validators.Length(min=5, max=120)])
    roles = MultiCheckboxField('Roles', choices=[])

class EditUserByAdminForm(FlaskForm):
    '''Formulario de edición de usuarios'''

    name = StringField('Nombre', [validators.InputRequired(), validators.Length(min=3, max=36)])
    lastname = StringField('Apellido', [validators.InputRequired(), validators.Length(min=3, max=40)])
    username = StringField('Nombre de usuario', [validators.InputRequired(), validators.Length(min=4, max=256)])
    email = StringField('Mail', [validators.InputRequired(), validators.Email(), validators.Length(min=6, max=120)])
    estado = SelectField('Estado actual', choices=[])
    roles = MultiCheckboxField('Roles', choices=[])


class EditProfileByAdminForm(FlaskForm):
    '''Formulario de edición de perfil de usuario logueado'''

    name = StringField('Nombre', [validators.InputRequired(), validators.Length(min=3, max=36)])
    lastname = StringField('Apellido', [validators.InputRequired(), validators.Length(min=3, max=40)])
    email = StringField('Mail', [validators.InputRequired(), validators.Email(), validators.Length(min=6, max=120)])
    roles = MultiCheckboxField('Roles', choices=[])
    
    
# Socios
class RegisterSocioForm(FlaskForm):
    '''Formulario de registro de socios'''

    name = StringField('Nombre (*)', [validators.InputRequired(), validators.Length(min=3, max=36)], render_kw={"placeholder": "Ingrese el nombre del socio"})
    lastname = StringField('Apellido (*)', [validators.InputRequired(), validators.Length(min=3, max=40)], render_kw={"placeholder": "Ingrese el apellido del socio"})
    email = StringField('Email', [validators.Optional(), validators.Email(), valid.validate_unique_email], render_kw={"placeholder": "Ingrese un email del socio"})
    type_ID = SelectField('Tipo de identificación (*)', choices=[])
    value_ID = StringField('Identificación (*)', [validators.InputRequired(), Regexp(regex='[0-9]+$'), valid.validate_unique_ID], render_kw={"placeholder": "Ingrese la identificación del socio"})
    gender = SelectField('Género (*)', choices=[])
    address = StringField('Domicilio (*)', [validators.InputRequired()], render_kw={"placeholder": "Ingrese el domicilio del socio"})
    phone = StringField('Teléfono', [validators.Optional(), validators.Length(min=10, max=18)], render_kw={"placeholder": "(+54) 221-000-0000"})
    disciplines = MultiCheckboxField('Disciplinas', choices=[])


# Disciplinas

class AltaDisciplinaForm(FlaskForm):
    '''Formulario de alta de disciplinas '''

    nombre_disciplina = StringField('Nombre disciplina',  [validators.data_required(), validators.length(max=50)],render_kw={"placeholder": "Basket"})
    costo = FloatField('Costo $', [validators.data_required()],render_kw={"placeholder": "750.75"})
    placeholder = 'Lunes a Viernes de 17 a 18'
    detalle = StringField('Dias y horarios', [validators.length(max=256)],widget=TextArea(), render_kw={"rows": 5, "cols": 20,"placeholder":placeholder})
    habilitada = BooleanField('Habilitada',default='checked')


class AltaInstructorForm(FlaskForm):
    '''Formulario de alta de instructores'''

    nombre_instructor = StringField('Nombre instructor', [validators.length(max=30)],render_kw={'placeholder':'Ingrese nombre'})
    apellido_instructor = StringField('Apellido instructor', [validators.length(max=30)],render_kw={'placeholder':'Ingrese apellido'})

class AltaCategoriaForm(FlaskForm):
    '''Formulario de alta de categorías'''

    placeholder =  'Pre-mini'
    descripcion = StringField('Categoria', [validators.data_required(),validators.length(max=128)],render_kw={'placeholder':placeholder})

class EditarDisciplinaForm(FlaskForm):
    '''Formulario de edición de disciplinas'''

    nombre_disciplina = StringField('Nombre disciplina',  [validators.data_required(), validators.length(max=50)],render_kw={"placeholder": "ingrese nombre"})
    costo = FloatField('Costo $', [validators.data_required()],render_kw={"placeholder": "750.75"})
    detalle = StringField('Dias y horarios', [validators.length(max=256)],widget=TextArea(), render_kw={"rows": 5, "cols": 20})
    habilitada = BooleanField('Habilitada',default='checked')