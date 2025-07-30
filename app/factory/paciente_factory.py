from app.models.paciente import Paciente
from .base_factory import PessoaFactory

class PacienteFactory:
    def criar(self, nome, data_nascimento, sexo, telefone, endereco):
        return Paciente(
            nome=nome,
            data_nascimento=data_nascimento,
            sexo=sexo,
            telefone=telefone,
            endereco=endereco
        )
