from app import db
from app.models.paciente import Paciente

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.Text)

    exames = db.relationship('Exame', backref='consulta', lazy=True)
    receitas = db.relationship('Receita', backref='consulta', lazy=True)
    




    def to_dict(self):
        return {
            "id": self.id,
            "id_paciente": self.id_paciente,
            "id_medico": self.id_medico,
            "data_consulta": str(self.data_consulta),
            "observacoes": self.observacoes
        }