from src.core import auth, business, roles, config, fees
import random, string
from datetime import datetime

def load_users():
    user1 = auth.load_user(
        password="1234",
        username="user1",
        nombre="User",
        email= "user@gmail.com",
        apellido="Superadmin" 
    )

    user2 = auth.load_user(
        password="1234",
        username="user2",
        nombre="User",
        email= "useroperador@gmail.com",
        apellido="Operador" 
    )
    
    for i in range(3, 31):
        apellido = ''.join(random.sample(string.ascii_lowercase,5))
        user = auth.load_user(
            password="1234",
            username="user{}".format(i),
            nombre="User",
            email= f"{apellido}@gmail.com",
            apellido=apellido
        )

    return user1, user2
    
def load_socios(disciplina1,disciplina2,disciplina3):
    socio1 = auth.load_socio(
       tipo_identificacion="DNI",
       identificacion="40000000",
       genero="Masculino",
       telefono="",
       email="socio1@gmail.com",
       nombre="socio1",
       apellido=''.join(random.sample(string.ascii_lowercase,5)).capitalize(),
       domicilio="525",
    )
    auth.update_socio_with_user(socio1.id, 'socio1', '1234')
    auth.assign_disciplinas(socio1, [disciplina1])
    for i in range(2, 31):
        socio = auth.load_socio(
            tipo_identificacion="DNI",
            identificacion="400000{0}{1}".format(i, i),
            genero=random.choice(["Masculino","Femenino",random.choice(["Otro","Masculino"])]),
            telefono="221{}{}{}{}{}{}".format(i,i,i,i,i,i),
            email="socio{}@gmail.com".format(i),
            nombre="socio{}".format(i),
            apellido= ''.join(random.sample(string.ascii_lowercase,5)).capitalize(),
            domicilio="525",
            fecha_alta = datetime.strptime(f'202{random.randrange(1,3)}-{random.randrange(1,13)}-2 13:45:21', '%Y-%m-%d %H:%M:%S').date() 
            )
        auth.assign_disciplinas(socio,[disciplina1,random.choice([disciplina2,disciplina3])])
    return socio1

def load_categorias():
        categorias = [business.load_categoria(
        descripcion = "Mini"
    ), business.load_categoria(
        descripcion = "infantil")]
        return categorias

def load_instructores():
    instructores = [business.load_instructor(
        nombre_instructor = "Alfredo",
        apellido_instructor = "Rodriguez"
    ), business.load_instructor(
        nombre_instructor = "Jose",
        apellido_instructor = "Perez"
    )]
    return instructores

def load_disciplinas():
        disciplina1 = business.load_disciplina(
        habilitada = True,
        detalle = "Lunes a Viernes de 18 a 19hs",
        nombre_disciplina = "Gimnasia deportiva",
        costo = 3000.5
        )
        disciplina2 = business.load_disciplina(
        habilitada = True,
        detalle = "Martes y Jueves de 17 a 18hs",
        nombre_disciplina = "Gimnasia artística",
        costo = 3000.5
        )
        disciplina3 = business.load_disciplina(
            habilitada = False,
            detalle = "Lunes a Viernes de 19 a 21hs",
            nombre_disciplina = "Futbol",
            costo = 2574.5
        )
        return disciplina1, disciplina2, disciplina3
    
def load_role():
    role1 = roles.load_role(
        nombre="ROL_ADMINISTRADOR"
    )
    
    role2 = roles.load_role(
        nombre="ROL_OPERADOR"
    )
    return role1, role2
    
def load_permissions():
    perms = []
    perms.append(roles.load_permission(nombre="socio_index"))
    perms.append(roles.load_permission(nombre="socio_new"))
    perms.append(roles.load_permission(nombre="socio_destroy"))
    perms.append(roles.load_permission(nombre="socio_update"))
    perms.append(roles.load_permission(nombre="socio_show"))
    perms.append(roles.load_permission(nombre="socio_switch_state"))
    perms.append(roles.load_permission(nombre="user_index"))
    perms.append(roles.load_permission(nombre="user_new"))
    perms.append(roles.load_permission(nombre="user_destroy"))
    perms.append(roles.load_permission(nombre="user_update"))
    perms.append(roles.load_permission(nombre="user_show"))
    perms.append(roles.load_permission(nombre="user_block"))
    perms.append(roles.load_permission(nombre="discipline_index"))
    perms.append(roles.load_permission(nombre="discipline_new"))
    perms.append(roles.load_permission(nombre="discipline_destroy"))
    perms.append(roles.load_permission(nombre="discipline_update"))
    perms.append(roles.load_permission(nombre="discipline_show"))
    perms.append(roles.load_permission(nombre="payments_index"))
    perms.append(roles.load_permission(nombre="payments_show"))
    perms.append(roles.load_permission(nombre="payments_import"))
    perms.append(roles.load_permission(nombre="payments_destroy"))
    perms.append(roles.load_permission(nombre="config"))
    perms.append(roles.load_permission(nombre="profile"))
    perms.append(roles.load_permission(nombre="api-rest-socio"))

    return perms

def load_configuration():
    config.load_configuration(cant_elem=10, pagos='Habilitada', email="clubdeportivovillaelisa@gmail.com",
                                phone="0221 487-0193", cuota_base=3500.70)
    
def load_cuotas():
    fees.generate_cuotas()

def run():
    user1, user2 = load_users()
        
    categorias = load_categorias()
    instructores = load_instructores()
    disciplinas = load_disciplinas()
    disciplina1, disciplina2, disciplina3 = disciplinas
    socio1 = load_socios(disciplina1,disciplina2,disciplina3)
    business.assign_instructores(disciplina1,instructores)
    business.assign_categorias(disciplina1,categorias)
    role1, role2 = load_role()
    perms = load_permissions()    
    business.assign_categorias(disciplina3,[categorias.pop()])
    instructores_futbol = instructores.pop()
    business.assign_instructores(disciplina3,[instructores_futbol])
    instructores_gim = instructores.pop()
    business.assign_instructores(disciplina2,[instructores_gim])
    categoria_gim = categorias.pop()
    business.assign_categorias(disciplina2,[categoria_gim])
    roles.assign_permissions(role1, perms) 
    lista_not_operator = ["switch_state", "block", "destroy"]
    perm2 = [perm for perm in perms if not any(x in perm.nombre for x in lista_not_operator)]
    roles.assign_permissions(role2, perm2)
    roles.assign_roles(user1, [role1])
    roles.assign_roles(user2, [role2])
    load_configuration()
    fees.generate_cuotas()

    print("Done!")