from app import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.Enum('M', 'F'), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.Text, nullable=False)

    consultas = db.relationship('Consulta', backref='paciente', lazy=True)

    @staticmethod
    def factory(nome, data_nascimento, sexo, telefone, endereco):
        return Paciente(
            nome=nome,
            data_nascimento=data_nascimento,
            sexo=sexo,
            telefone=telefone,
            endereco=endereco
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": str(self.data_nascimento),
            "sexo": self.sexo,
            "telefone": self.telefone,
            "endereco": self.endereco
        }
