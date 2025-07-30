from models.pagamento import Pagamento

class PagamentoFactory:
    @staticmethod
    def criar_pagamento(id_consulta, valor, forma_pagamento, status_pagamento='Pendente'):
        return Pagamento(
            id_consulta=id_consulta,
            valor=valor,
            forma_pagamento=forma_pagamento,
            status_pagamento=status_pagamento
        )
