from app.extensions import db  # <--- NÃO importa mais de app

from .usuario import Usuario
from .paciente import Paciente
from .medico import Medico
from .consulta import Consulta
from .exame import Exame
from .receita import Receita
from .pagamento import Pagamento


def register_models():
    pass
