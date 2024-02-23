from src.core.business import get_all_disciplinas
from src.core.roles import list_roles

def load_genders():
    return [('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Otro', 'Otro')]

def load_disciplinas():
    return [(elem.nombre_disciplina, elem.nombre_disciplina) for elem in get_all_disciplinas()]

def load_type_id():
    return [('DNI', 'DNI'), ('CUIL', 'CUIL')]

def load_roles():
    return [(elem.nombre, elem.nombre) for elem in list_roles()]

def load_roles_without_admin():
    return [(elem.nombre, elem.nombre) for elem in list_roles() if elem.nombre != 'ROL_ADMINISTRADOR']
    
def load_state():
    return [('all', 'Todos'), ('active', 'Activo'), ('inactive', 'No activo')]

def load_tabla_pagos():
    return [('Habilitar', 'Habilitar'), ('Deshabilitar', 'Deshabilitar')]

def load_elem_per_page():
    return [('10', '10'), ('20', '20'), ('30', '30')]

def load_criterio():
    return [('asc', 'Ascendente'), ('desc', 'Descendente')]

def load_user_estados():
    return [('True', 'Activo'), ('False', 'Bloqueado')]

def load_socio_estados():
    return [('True', 'No bloqueado'), ('False', 'Bloqueado')]
