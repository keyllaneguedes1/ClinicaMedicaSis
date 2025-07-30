from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.facade.clinica_facade import ClinicaFacade

pagamento_bp = Blueprint('pagamento_bp', __name__)

@pagamento_bp.route('/pagamentos')
def listar_pagamentos():
    pagamentos = ClinicaFacade.listar_pagamentos()
    return render_template('pagamentos/listar_pagamentos.html', pagamentos=pagamentos)

@pagamento_bp.route('/pagamentos/novo', methods=['GET', 'POST'])
def novo_pagamento():
    if request.method == 'POST':
        try:
            ClinicaFacade.criar_pagamento(
                id_consulta=int(request.form['id_consulta']),
                valor=float(request.form['valor']),
                forma_pagamento=request.form['forma_pagamento'],
                status_pagamento=request.form.get('status_pagamento', 'Pendente')
            )
            flash('Pagamento criado com sucesso!', 'success')
            return redirect(url_for('pagamento_bp.listar_pagamentos'))

        except ValueError as ve:
            flash(str(ve), 'danger')  # Mostra mensagem de erro ao usuário

        except Exception:
            flash('Erro interno ao criar o pagamento.', 'danger')

    return render_template('pagamentos/novo_pagamento.html')

@pagamento_bp.route('/pagamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_pagamento(id):
    pagamento = ClinicaFacade.buscar_pagamento(id)

    if request.method == 'POST':
        ClinicaFacade.editar_pagamento(
            id=id,
            valor=float(request.form['valor']),
            forma_pagamento=request.form['forma_pagamento'],
            status_pagamento=request.form['status_pagamento']
        )
        return redirect(url_for('pagamento_bp.listar_pagamentos'))

    return render_template('pagamentos/editar_pagamento.html', pagamento=pagamento)

@pagamento_bp.route('/pagamentos/excluir/<int:id>', methods=['POST'])
def excluir_pagamento(id):
    ClinicaFacade.excluir_pagamento(id)
    return redirect(url_for('pagamento_bp.listar_pagamentos'))


