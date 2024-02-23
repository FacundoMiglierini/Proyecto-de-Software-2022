from src.core.database import db
from src.core.roles.models import Role, Permission
from src.core.auth import User

def load_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    
    return role

def load_permission(**kwargs):
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
    
    return permission

def assign_roles(user, roles):
    user.roles.extend(roles)
    db.session.add(user)
    db.session.commit()
    
    return user

def assign_permissions(role, permissions):
    role.permisos.extend(permissions)
    db.session.add(role)
    db.session.commit()
    
    return role

def role_has_permission(role, permission):
    '''Chequea si el role tiene un permission asignado'''
    
    for perm in role.permisos:
        if perm.nombre == permission:
            return True
    return False    


def list_roles():
    return Role.query.all()

def list_permissions():
    return Permission.query.all()

def get_rol_by_name(nombre):
    '''Retorna un rol por su nombre, en caso de existir. De lo contrario, retorna None'''

    return Role.query.filter_by(nombre=nombre).first()

def get_roles_from_user(id):
    """Retorna los roles que tiene asignados un usuario a través de su id"""

    prueba = Role.query.join(Role.users).filter(User.id == id)
    return prueba