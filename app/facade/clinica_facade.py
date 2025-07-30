from app.models import db, Paciente, Medico, Consulta, Exame, Receita, Usuario, Pagamento
from datetime import datetime
from app.factory.paciente_factory import PacienteFactory
from app.factory.medico_factory import MedicoFactory
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from sqlalchemy.exc import DBAPIError
from sqlalchemy import text

class ClinicaFacade:
    def __init__(self):
        self.paciente_factory = PacienteFactory()
        self.medico_factory = MedicoFactory()

    # ----------------------- PACIENTES -----------------------

    def cadastrar_paciente(self, nome, data_nascimento, sexo, telefone, endereco):
        try:
            paciente = self.paciente_factory.criar(nome, data_nascimento, sexo, telefone, endereco)
            db.session.add(paciente)
            db.session.commit()
            return paciente
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao cadastrar paciente: {e}")
            return None

    def listar_pacientes(self):
        return Paciente.query.all()

    def buscar_paciente_por_id(self, id):
        return Paciente.query.get(id)

    def atualizar_paciente(self, paciente, data):
        try:
            paciente.nome = data.get('nome', paciente.nome)
            paciente.cpf = data.get('cpf', paciente.cpf)
            paciente.data_nascimento = data.get('data_nascimento', paciente.data_nascimento)
            paciente.sexo = data.get('sexo', paciente.sexo)
            paciente.telefone = data.get('telefone', paciente.telefone)
            paciente.endereco = data.get('endereco', paciente.endereco)
            db.session.commit()
            return paciente
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao atualizar paciente: {e}")
            return None

    def deletar_paciente(self, paciente):
        try:
            db.session.delete(paciente)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao deletar paciente: {e}")
            return False

    # ----------------------- MÉDICOS -----------------------

    def cadastrar_medico(self, nome, crm, especialidade, telefone):
        try:
            medico = self.medico_factory.criar(nome, crm, especialidade, telefone)
            db.session.add(medico)
            db.session.commit()
            return medico
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao cadastrar médico: {e}")
            return None

    def listar_medicos(self):
        return Medico.query.all()

    def buscar_medico_por_id(self, id):
        return Medico.query.get(id)

    def atualizar_medico(self, medico, data):
        try:
            medico.nome = data.get('nome', medico.nome)
            medico.crm = data.get('crm', medico.crm)
            medico.especialidade = data.get('especialidade', medico.especialidade)
            db.session.commit()
            return medico
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao atualizar médico: {e}")
            return None

    def deletar_medico(self, medico):
        try:
            db.session.delete(medico)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao deletar médico: {e}")
            return False

    # ----------------------- CONSULTAS -----------------------

    def listar_consultas(self):
        return Consulta.query.order_by(Consulta.data_consulta.desc()).all()

   

    def marcar_consulta(self, id_paciente, id_medico, data_consulta, observacoes=None):
        try:
            sql = text("CALL sp_cadastrar_consulta(:id_paciente, :id_medico, :data_consulta, :observacoes)")
            db.session.execute(sql, {
                "id_paciente": id_paciente,
                "id_medico": id_medico,
                "data_consulta": data_consulta,
                "observacoes": observacoes
            })
            db.session.commit()
            return "sucesso"
        except DBAPIError as e:
            db.session.rollback()
            if e.orig and 'Conflito de agenda' in str(e.orig):
                print("Erro: Este horário já está reservado para o médico.")
                return "conflito"
            print(f"Erro ao marcar consulta: {e}")
            return "erro"

    
    def atualizar_consulta(self, id, id_paciente, id_medico, data_consulta, observacoes):
        consulta = Consulta.query.get(id)
        if not consulta:
            return None
        consulta.id_paciente = id_paciente
        consulta.id_medico = id_medico
        consulta.data = data_consulta
        consulta.observacoes = observacoes
        db.session.commit()
        return consulta
    
    def buscar_consulta_por_id(self, id):
        return Consulta.query.get(id)

    def deletar_consulta(self, id_consulta, forcar=False):
        try:
            consulta = Consulta.query.get(id_consulta)
            if not consulta:
                raise ValueError("Consulta não encontrada.")

            if consulta.pagamento and not forcar:
                raise ValueError("⚠️ Esta consulta já possui pagamento registrado. Tem certeza que deseja excluir mesmo assim?")

            db.session.delete(consulta)
            db.session.commit()
            return True
        except ValueError as ve:
            return str(ve)
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Erro ao excluir consulta: {e}"




    # ----------------------- EXAMES -----------------------

    def listar_exames(self):
        return Exame.query.all()

    def criar_exame(self, dados):
        exame = Exame(**dados)
        db.session.add(exame)
        db.session.commit()
        return exame

    # ----------------------- RECEITAS -----------------------

    def listar_receitas(self):
        return Receita.query.all()

    def criar_receita(self, dados):
        receita = Receita(**dados)
        db.session.add(receita)
        db.session.commit()
        return receita

    # ----------------------- USUÁRIOS -----------------------

    def listar_usuarios(self):
        return Usuario.query.all()

    def criar_usuario(self, dados):
        usuario = Usuario(**dados)
        db.session.add(usuario)
        db.session.commit()
        return usuario
    # ----------------------- PAGAMENTOS -----------------------
    @staticmethod
    def listar_pagamentos():
        return Pagamento.query.all()
    
    
    @staticmethod
    def criar_pagamento(id_consulta, valor, forma_pagamento, status_pagamento='Pendente'):
        try:
            # Verifica se a consulta existe antes de criar o pagamento
            consulta = db.session.get(Consulta, id_consulta)
            if not consulta:
                raise ValueError(f"Consulta com ID {id_consulta} não encontrada")
            
            # Cria o objeto de pagamento
            novo_pagamento = Pagamento(
                id_consulta=id_consulta,
                valor=valor,
                forma_pagamento=forma_pagamento,
                status_pagamento=status_pagamento,
                data_pagamento=datetime.utcnow() if status_pagamento == 'Pago' else None
            )
            
            db.session.add(novo_pagamento)
            db.session.commit()
            return novo_pagamento
            
        except IntegrityError as e:
            db.session.rollback()
            # Verifica se o erro é específico de foreign key
            if "foreign key constraint fails" in str(e.orig):
                raise ValueError(f"Consulta com ID {id_consulta} não existe ou é inválida") from e
            raise  # Re-lança outros tipos de IntegrityError
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def buscar_pagamento(id):
        return Pagamento.query.get(id)


    
    @staticmethod
    def excluir_pagamento(id):
        pagamento = Pagamento.query.get(id)
        if pagamento:
            db.session.delete(pagamento)
            db.session.commit()
        return pagamento
    
    @staticmethod
    def editar_pagamento(id, valor, forma_pagamento, status_pagamento):
        pagamento = Pagamento.query.get(id)
        if not pagamento:
            raise ValueError(f"Pagamento com ID {id} não encontrado")
        
        pagamento.valor = valor
        pagamento.forma_pagamento = forma_pagamento
        pagamento.status_pagamento = status_pagamento
        
        # Atualiza a data_pagamento se status mudou para 'Pago'
        if status_pagamento == 'Pago' and not pagamento.data_pagamento:
            from datetime import datetime
            pagamento.data_pagamento = datetime.now()
        elif status_pagamento != 'Pago':
            pagamento.data_pagamento = None

        db.session.commit()
        return pagamento
    # ----------------------- PROCEDURES E VIEWS -----------------------

    def historico_paciente_procedure(self, id_paciente):
        sql = text("CALL sp_historico_paciente(:pid)")
        result = db.session.execute(sql, {"pid": id_paciente})
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]

    def consultas_por_medico_procedure(self, id_medico, data_inicio, data_fim):
        sql = text("CALL sp_consultas_por_medico(:mid, :inicio, :fim)")
        result = db.session.execute(sql, {"mid": id_medico, "inicio": data_inicio, "fim": data_fim})
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]
    
    def historico_pacientes_view(self):
        sql = text("SELECT * FROM vw_historico_pacientes")
        result = db.session.execute(sql)
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]

    def consultas_completas_view(self):
        sql = text("SELECT * FROM vw_consultas_completas")
        result = db.session.execute(sql)
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]
    

    def gerar_relatorio_pagamentos(self, data_inicio, data_fim):
        try:
            sql = text("CALL sp_relatorio_pagamentos(:data_inicio, :data_fim)")
            result = db.session.execute(sql, {"data_inicio": data_inicio, "data_fim": data_fim})
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result.fetchall()]
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            return None
        
    def consultas_por_periodo(self, data_inicio, data_fim):
        sql = text("""
            SELECT * FROM vw_consultas_por_data
            WHERE DATE(data_consulta) BETWEEN :inicio AND :fim
        """)
        result = db.session.execute(sql, {"inicio": data_inicio, "fim": data_fim})
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]



