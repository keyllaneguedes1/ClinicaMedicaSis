from app.models.medico import Medico
from .base_factory import PessoaFactory

class MedicoFactory(PessoaFactory):
    def criar(self, nome, especialidade, crm, telefone):
        return Medico(
            nome=nome,
            especialidade=especialidade,
            crm=crm,
            telefone=telefone
        )
