from app import db
from datetime import datetime

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.Enum('Dinheiro', 'Cartão', 'Pix', 'Convênio'), nullable=False)
    status_pagamento = db.Column(db.Enum('Pendente', 'Pago', 'Cancelado'), default='Pendente')
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)

    
    consulta = db.relationship('Consulta', backref=db.backref('pagamento', uselist=False))

     

    def to_dict(self):
        return {
            "id": self.id,
            "id_consulta": self.id_consulta,
            "valor": str(self.valor),
            "forma_pagamento": self.forma_pagamento,
            "status_pagamento": self.status_pagamento,
            "data_pagamento": self.data_pagamento.isoformat() if self.data_pagamento else None
        }