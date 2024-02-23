from sqlite3 import SQLITE_SELECT
from src.core.database import db
from src.core.business.models import Disciplina, Instructor, Categoria, disciplina_categoria

def list_disciplinas():
    '''Devuelve todas las disciplinas'''
    return Disciplina.query.all()

def load_instructor(**kwargs):
    '''carga un instructor en la bd con los parametros recibidos'''
    instructor = Instructor(**kwargs)
    db.session.add(instructor)
    db.session.commit()

    return instructor

def load_categoria(**kwargs):
    '''Carga una categoria en la bd con los parametros recibidos'''
    categoria = Categoria(**kwargs)
    db.session.add(categoria)
    db.session.commit()

    return categoria

def load_disciplina(**kwargs):
    '''Carga una disciplina en la bd con los parametros recibidos'''
    disciplina = Disciplina(**kwargs)
    db.session.add(disciplina)
    db.session.commit()

    return disciplina

def assign_categorias(disciplina, categorias):
    '''Asigna el listado de categorias recibidas a la disciplina recibida'''
    disciplina.categorias.extend(categorias)
    db.session.add(disciplina)
    db.session.commit()

    return disciplina

def assign_instructores(disciplina, instructores):
    '''Asigna la lista de instructores recibida a la disciplina recibida'''
    disciplina.instructores.extend(instructores)
    db.session.add(disciplina)
    db.session.commit()

    return disciplina

def unlink_categorias(disciplina,categoria):
    '''Desvincula la categoria recibida de la disciplina recibida'''
    disciplina.categorias.remove(categoria)
    db.session.add(disciplina)
    db.session.commit()

def get_instructor(nombre,apellido):
    '''Devuelve un instructor que contenga el nombre y apellido recibidos'''
    instructor = Instructor()
    instructor = db.session.query(Instructor).filter(Instructor.apellido_instructor.like(apellido),
                                                Instructor.nombre_instructor.like(nombre)).first()
    return instructor

def unlink_instructor(disciplina,instructor):
    """Desvincula instructores de disciplina, recibidos por parámetro"""
    disciplina.instructores.remove(instructor)
    db.session.add(disciplina)
    db.session.commit()

def get_categoria(descripcion):
    """Retorna una categoría a partir de una descripción recibida por parámetro, en caso de que exista"""
    categoria = Categoria()
    categoria = db.session.query(Categoria).filter(Categoria.descripcion == descripcion).first()

    return categoria

def get_disciplina(nombre):
    """Retorna la disciplina cuyo nombre coincida con el string recibido por párametro, si existe"""
    disciplina = Disciplina.query.filter_by(nombre_disciplina=nombre).first()
    return disciplina
    
def get_all_disciplinas():
    return Disciplina.query.all()

def disciplina_exists(nombre):
    """Retorna True si la disciplina existe, False si no"""
    return get_disciplina(nombre) != None

def list_disciplinas_categorias_instructor():
    disciplinas = Disciplina()
    disciplinas = (db.session.query(Disciplina).outerjoin(Categoria,Disciplina.categorias).
                outerjoin(Instructor,Disciplina.instructores))
    return disciplinas

def get_disciplina_by_id(id):
    disciplina = db.session.query(Disciplina).get(id)

    return disciplina

def update_disciplina(disciplina):
    db.session.add(disciplina)
    db.session.commit()

    return disciplina

def delete_disciplina(disciplina):
    db.session.delete(disciplina)
    db.session.commit()

def list_categorias_from_disciplina_id(id):
    categorias = db.session.query(Disciplina).filter(id == Disciplina.id).outerjoin(Categoria,Disciplina.categorias)
    return categorias

def get_categoria_by_id(id):
    categoria = db.session.query(Categoria).get(id)

    return categoria

def get_instructor_by_id(id):
    instructor = db.session.query(Instructor).get(id)

    return instructor

def list_instructores_from_disciplina_id(id):
    instructores = Instructor()
    instructores = (db.session.query(Disciplina).filter(id== Disciplina.id).outerjoin(Instructor,Disciplina.instructores))

    return instructores
