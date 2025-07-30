from app import db

class Medico(db.Model):
    __tablename__ = 'medicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    consultas = db.relationship('Consulta', backref='medico', lazy=True)

    @staticmethod
    def factory(nome, especialidade, crm, telefone):
        return Medico(nome=nome, especialidade=especialidade, crm=crm, telefone=telefone)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especialidade": self.especialidade,
            "crm": self.crm,
            "telefone": self.telefone
        }
