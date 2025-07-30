from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.facade.clinica_facade import ClinicaFacade
from app.models.exame import Exame
from app.models.consulta import Consulta
from app import db

exame_bp = Blueprint('exame', __name__)
facade = ClinicaFacade()

# LISTAR
@exame_bp.route('/exames')
def listar_exames():
    exames = facade.listar_exames()
    return render_template('exames/listar.html', exames=exames)

# FORMULÁRIO DE CRIAÇÃO
@exame_bp.route('/exames/novo')
def novo_exame():
    consultas = facade.listar_consultas()
    return render_template('exames/novo.html', consultas=consultas)

# CRIAR
@exame_bp.route('/exames/criar', methods=['POST'])
def criar_exame():
    try:
        id_consulta = request.form['id_consulta']
        tipo_exame = request.form['tipo_exame']
        resultado = request.form['resultado']
        facade.criar_exame({
            'id_consulta': id_consulta,
            'tipo_exame': tipo_exame,
            'resultado': resultado
        })
        flash('Exame criado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao criar exame: {e}', 'danger')
    return redirect(url_for('exame.listar_exames'))

# EDITAR (FORMULÁRIO)
@exame_bp.route('/exames/editar/<int:id>')
def editar_exame(id):
    exame = Exame.query.get_or_404(id)
    consultas = facade.listar_consultas()
    return render_template('exames/editar.html', exame=exame, consultas=consultas)

# ATUALIZAR
@exame_bp.route('/exames/atualizar/<int:id>', methods=['POST'])
def atualizar_exame(id):
    try:
        exame = Exame.query.get_or_404(id)
        exame.id_consulta = request.form['id_consulta']
        exame.tipo_exame = request.form['tipo_exame']
        exame.resultado = request.form['resultado']
        db.session.commit()
        flash('Exame atualizado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar exame: {e}', 'danger')
    return redirect(url_for('exame.listar_exames'))

# DELETAR
@exame_bp.route('/exames/deletar/<int:id>', methods=['POST'])
def deletar_exame(id):
    try:
        exame = Exame.query.get_or_404(id)
        db.session.delete(exame)
        db.session.commit()
        flash('Exame deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar exame: {e}', 'danger')
    return redirect(url_for('exame.listar_exames'))
