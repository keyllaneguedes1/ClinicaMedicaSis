from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.facade.clinica_facade import ClinicaFacade
from app.models.medico import Medico
from app import db

medico_bp = Blueprint('medico', __name__)
facade = ClinicaFacade()

# Rota para listar todos os médicos
@medico_bp.route('/medicos', methods=['GET'])
def listar_medicos():
    medicos = facade.listar_medicos()
    return render_template('medicos/medicos.html', medicos=medicos)


# Rota para exibir e processar formulário de cadastro
@medico_bp.route('/medicos/novo', methods=['GET', 'POST'])
def cadastrar_medico():
    if request.method == 'POST':
        nome = request.form.get('nome')
        crm = request.form.get('crm')
        especialidade = request.form.get('especialidade')
        telefone = request.form.get('telefone')

        medico = facade.cadastrar_medico(nome, crm, especialidade, telefone)

        if medico:
            flash('Médico cadastrado com sucesso!', 'success')
            return redirect(url_for('medico.listar_medicos'))
        else:
            flash('Erro ao cadastrar médico.', 'danger')
            return redirect(url_for('medico.cadastrar_medico'))

    return render_template('medicos/novo_medico.html')


# Rota para editar dados de um médico
@medico_bp.route('/medicos/editar/<int:id>', methods=['GET', 'POST'])
def editar_medico(id):
    medico = Medico.query.get_or_404(id)

    if request.method == 'POST':
        medico.nome = request.form.get('nome', medico.nome)
        medico.crm = request.form.get('crm', medico.crm)
        medico.especialidade = request.form.get('especialidade', medico.especialidade)
        medico.telefone = request.form.get('telefone', medico.telefone)

        try:
            db.session.commit()
            flash('Médico atualizado com sucesso!', 'success')
            return redirect(url_for('medico.listar_medicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar médico: {e}', 'danger')
            return render_template('medicos/editar_medico.html', medico=medico)

    return render_template('medicos/editar_medico.html', medico=medico)


# Rota para excluir um médico
@medico_bp.route('/medicos/deletar/<int:id>', methods=['POST'])
def deletar_medico(id):
    medico = Medico.query.get_or_404(id)

    try:
        db.session.delete(medico)
        db.session.commit()
        flash('Médico excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir médico: {e}', 'danger')

    return redirect(url_for('medico.listar_medicos'))
