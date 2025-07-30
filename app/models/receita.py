from app import db

class Receita(db.Model):
    __tablename__ = 'receitas'

    id = db.Column(db.Integer, primary_key=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    medicamento = db.Column(db.String(100), nullable=False)
    posologia = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_consulta": self.id_consulta,
            "medicamento": self.medicamento,
            "posologia": self.posologia
        }