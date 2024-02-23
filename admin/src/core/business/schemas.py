from src.core.business.models import Disciplina, Instructor, Categoria
from src.core.database import ma

class InstructorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Instructor
        fields = ('nombre_instructor', 'apellido_instructor')
        
class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria
        fields = ('descripcion',)

class DisciplinaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Disciplina

    id = ma.auto_field()
    detalle = ma.auto_field()
    costo = ma.auto_field()
    categorias = ma.auto_field()
    instructores = ma.Nested(InstructorSchema,many=True)
    categorias = ma.Nested(CategoriaSchema,many=True)
    nombre_disciplina = ma.auto_field()
    