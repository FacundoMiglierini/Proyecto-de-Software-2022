from flask import Blueprint
from src.core.business import list_disciplinas_categorias_instructor
from src.core.business import list_disciplinas
from src.core.auth import cant_socios_por_disciplina_id
from src.core.auth import get_socios_genero_disciplina,cant_socios_por_mes
from src.core.auth import get_socios_genero_club
from src.core.config import get_contact
from src.core.config.schemas import ContactoSchema
from src.core.business.schemas import DisciplinaSchema
from src.core.config import get_contact
from src.core.config.schemas import ContactoSchema
from flask import jsonify
from datetime import datetime


api_club_blueprint = Blueprint("api_club", __name__, url_prefix="/api/club")


@api_club_blueprint.get("/info")
def info():
   contact = get_contact() 
   contact_schema = ContactoSchema()
   return contact_schema.dump(contact)

@api_club_blueprint.get("/disciplinas")
def disciplinas():
   disciplinas = list_disciplinas_categorias_instructor()
   disciplinas_schema = DisciplinaSchema()
   listado = []
   for disciplina in disciplinas:
      dump = disciplinas_schema.dump(disciplina)
      dump['costo'] = '$' + str(dump['costo'])
      listado.append(dump)

   return listado

@api_club_blueprint.get("/stats/gender")
def gender():
   genders = get_socios_genero_disciplina()
   listado = []
   for elem in genders:
      dic = {}
      dic["genero"] = elem[0]
      dic["disciplina"] = elem[1]
      dic["cant"] = elem[2]
      listado.append(dic)

   return jsonify(listado)

@api_club_blueprint.get("/stats/gender_all")
def gender_all():
   genders = get_socios_genero_club()
   
   data = []
   labels = []
   for elem in genders:
      labels.append(elem[0])
      data.append(elem[1])
   for elem in ['Masculino', 'Femenino', 'Otro']:
      if elem not in labels:
         labels.append(elem)
         data.append(0)
   
   dic = {'labels' : labels, 'data': data}

   return jsonify(dic)

@api_club_blueprint.get("/stats/deportistas")
def cant_deportistas():
   disciplinas = list_disciplinas()
   labels = []
   data = []
   for elem in disciplinas:
      labels.append(elem.nombre_disciplina)
      data.append(cant_socios_por_disciplina_id(elem.id))
   

   dic = {'labels': labels, 'data': data}

   return jsonify(dic)

@api_club_blueprint.get("/stats/socios")
def cant_socios():
   '''devuelve en formato JSON la cantidad de socios inscriptos en los ultimos 24 meses'''
   mes = datetime.now().month
   año = datetime.now().year - 2
   data = []
   labels = []
   meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
      "Octubre", "Noviembre", "Diciembre"]
   for i in range(0,24):
      mes = mes + 1
      if mes == 13:
         mes = 1
         año = año + 1
      labels.append(str(meses[mes - 1] + " " + str(año)))
      data.append(cant_socios_por_mes(mes,año))
   dic = {'labels': labels, 'data':data}
   return jsonify(dic)
   