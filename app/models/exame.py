from app import db

class Exame(db.Model):
    __tablename__ = 'exames'

    id = db.Column(db.Integer, primary_key=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    tipo_exame = db.Column(db.String(100), nullable=False)
    resultado = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "id_consulta": self.id_consulta,
            "tipo_exame": self.tipo_exame,
            "resultado": self.resultado
        }