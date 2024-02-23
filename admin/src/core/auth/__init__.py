from datetime import datetime
from flask import session
from sqlalchemy import func,extract
import hashlib
from src.core.database import db
from src.core.auth.models import User, Socio, socio_disciplina
from src.core.business.models import Disciplina


def list_users():
    query = User.query.filter(User.id != 1).filter(User.username != session["username"]) # Filtro a user administrador y user logueado
    return query

def list_socios():
    return Socio.query.order_by(Socio.id.asc())

def load_user(**kwargs):
    kwargs["password"] = hashlib.sha256(kwargs["password"].encode()).hexdigest() 
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def load_socio(**kwargs):
    socio = Socio(**kwargs)
    db.session.add(socio)
    db.session.commit()

    return socio

def assign_disciplinas(socio, disciplinas):
    socio.disciplinas.extend(disciplinas)
    db.session.add(socio)
    db.session.commit()

    return socio

def get_user_by_username(username):
    '''Retorna user por su username, en caso de existir. De lo contrario, retorna None'''

    return User.query.filter_by(username=username).first()

def get_exact_user(username, email):
    '''Retorna user por un string presente en su username o su email, en caso de existir. De lo contrario, retorna None'''
    user = User()
    user = db.session.query(User).filter(User.username.like(username) | User.email.like(email)).first()

    return user

def get_user_id(id):
    '''Retorna un usuario con el id ingresado, en caso de que exista'''
    user = User.query.get(id)

    return user

def get_by_search_string(users,string):
    '''Retorna un filtrado de listado de usuarios con el string ingresado presente en su email, en caso de que exista'''
    search = "%{}%".format(string.lower())

    return users.filter(User.email.ilike(search))

def get_by_estado(users,estado):
    '''Retorna un filtrado de listado de usuarios con el estado recibido por parámetro, en caso de que exista'''

    return users.filter(User.estado == estado)

def get_socios_by_search_string(socios, string):
    '''Retorna un filtrado de listado de socios con el string ingresado presente en su apellido, en caso de que exista'''
    search = "%{}%".format(string.lower())

    return socios.filter(Socio.apellido.ilike(search))

def get_socio_id(id):
    '''Retorna un socio con el id ingresado, en caso de que exista'''
    
    return Socio.query.get(id)

def get_socio(identificacion):
    '''Retorna un socio con la identificación ingresada, en caso de que exista'''

    return Socio.query.filter_by(identificacion=identificacion).first()

def get_socio_email(email):
    '''Retorna un socio con el email ingresado, en caso de que exista'''

    email = email.lower()

    return Socio.query.filter_by(email=email).first()

def get_all_socios(state=None, last_name=None):
    '''Retorna todos los socios cargados en la BD, ordenados por su número de socio.
    Si se agrega el parámetro "state", va a filtrar por el estado del socio.
    Si se agrega el parámetro "last_name", va a filtrar por apellido del socio.
    Si se agregan ambos parámetros, se filtrará por ambos criterios.'''

    socios_list = Socio.query

    if last_name:
        socios_list = get_socios_by_search_string(socios_list, last_name)
    
    if state is not None:
        socios_list = socios_format(socios_list)
        if state != 'todos':
            if state == 'True':
                socios_list = socios_list.filter_by(estado = 'Impaga') #Inactivos
            else:
                socios_list = socios_list.filter_by(estado = None) #Activos

    return socios_list
    
def get_socios_by_lastname_or_id(input):
    '''Retorna la cantidad de socios que tienen el id o el apellido indicado por input.
    Además, si el input es id retorna True. Si el input es apellido, retorna false.'''

    if(input.isdigit()):
        input = int(input)
        socios = Socio.query.get(input)
        cant = 1 if socios is not None else 0
        id = True
    else:
        input = input.capitalize()
        socios = Socio.query.filter_by(apellido=input)
        id = False
        cant = socios.count()

    return cant, id

def find_user_by_username_and_pass(username, password):
    '''Retorna al usuario con el username y password indicados'''

    password = hashlib.sha256(password.encode()).hexdigest()
    
    return User.query.filter_by(username=username, password=password).first()

def find_socio_by_username_and_pass(username, password):
    '''Retorna al socio con el username y password indicados'''

    password = hashlib.sha256(password.encode()).hexdigest()

    return Socio.query.filter_by(username=username, password=password).first()

def get_disciplinas_from_socio(id):
    """Retorna las disciplinas en las que esta inscripto un socio"""

    mis_disciplinas = db.session.query(Socio).filter(id == Socio.id).outerjoin(Disciplina,Socio.disciplinas)

    return mis_disciplinas

def update_socio(socio_with_new_data):
    '''Actualiza un socio recibido por parámetro en la base de datos'''

    db.session.add(socio_with_new_data)
    db.session.commit()

def update_socio_with_user(socio_id, username, password):
    socio = get_socio_id(socio_id)
    socio.password = hashlib.sha256(password.encode()).hexdigest()
    socio.username = username

    update_socio(socio)

def update_user(user_with_new_data):
    '''Actualiza un usuario recibido por parámetro en la base de datos'''

    db.session.add(user_with_new_data)
    db.session.commit()

def delete_user(id):
    '''Elimina un usuario con el id recibido por parámetro de la base de datos'''
    
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

def delete_socio(id):
    '''Elimina un socio recibido por parámetro de la base de datos'''
    
    socio = Socio.query.get(id)
    db.session.delete(socio)
    db.session.commit()

def socios_format(socios):
    '''Se preparan los datos a mostrar en el listado de socios.'''
    from src.core.fees.models import Cuota

    primer_dia_venc = datetime(datetime.now().year, datetime.now().month, 1)
    cuotas = db.session.query(Cuota.socio_id, Cuota.estado, Cuota.created_at).filter(Cuota.estado == "Impaga").filter(Cuota.created_at < primer_dia_venc).distinct(Cuota.socio_id).subquery()
    socios = socios.subquery()
    socios_cuotas = db.session.query(socios.c.id, socios.c.nombre, socios.c.apellido, socios.c.tipo_identificacion, socios.c.identificacion, socios.c.domicilio, socios.c.username, socios.c.password, socios.c.estado_act_block, socios.c.telefono, socios.c.email, cuotas.c.estado).outerjoin(cuotas, cuotas.c.socio_id == socios.c.id) 

    return socios_cuotas


def get_socios_sin_disciplina(socios, id):
    '''Retorna los socios recibidos en "socios" que no posean la disciplina indicada por "id".'''

    socios = socios.subquery()
    socios_disciplina = db.session.query(socio_disciplina.c.id_socio).filter(socio_disciplina.c.id_disciplina==id)
    socios = db.session.query(socios).filter(socios.c.id.not_in(socios_disciplina))

    return socios

def get_socios_genero_disciplina():
    '''Retorna la cantidad de socios por género por disciplina'''

    return db.session.query(Socio.genero, Disciplina.nombre_disciplina, func.count(Socio.genero)).join(Disciplina, Socio.disciplinas)\
                .group_by(Socio.genero, Disciplina.nombre_disciplina).all()


def get_socios_genero_club():
    '''Retorna la cantidad de socios por género que practican una disciplina en el club'''

    return db.session.query(Socio.genero, func.count(Socio.genero)).join(Disciplina, Socio.disciplinas)\
                .group_by(Socio.genero).all()

def cant_socios_por_disciplina_id(id):
    '''Retorna la cantidad de socios anotados en una disciplina cuyo id se recibe como parametro'''

    return db.session.query(Socio).join(Socio.disciplinas).filter(Disciplina.id==id).count()

def cant_socios_por_mes(mes,año):
    '''Retorna la cantidad total de socios inscriptos en el mes y año recibido como parametro'''
    
    return db.session.query(Socio).filter(extract('month',Socio.fecha_alta) == mes, extract('year',Socio.fecha_alta) == año).count()