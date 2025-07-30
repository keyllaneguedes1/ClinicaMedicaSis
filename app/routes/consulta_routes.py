from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.facade.clinica_facade import ClinicaFacade
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.consulta import Consulta

consulta_bp = Blueprint('consulta', __name__)
facade = ClinicaFacade()

# Listar consultas - HTML
@consulta_bp.route('/consultas', methods=['GET'])
def listar_consultas():
    consultas = facade.listar_consultas()
    pacientes = facade.listar_pacientes()
    medicos = facade.listar_medicos()
    return render_template('consultas/consultas.html', consultas=consultas, pacientes=pacientes, medicos=medicos)


# Formulário para nova consulta - GET
@consulta_bp.route('/consultas/nova', methods=['GET'])
def nova_consulta():
    pacientes = facade.listar_pacientes()
    medicos = facade.listar_medicos()
    return render_template('consultas/nova_consulta.html', pacientes=pacientes, medicos=medicos)


# Criar nova consulta - POST
@consulta_bp.route('/consultas/nova', methods=['POST'])
def cadastrar_consulta():
    id_paciente = request.form.get('id_paciente')
    id_medico = request.form.get('id_medico')
    data_consulta = request.form.get('data_consulta')
    observacoes = request.form.get('observacoes')

    resultado = facade.marcar_consulta(
        id_paciente=id_paciente,
        id_medico=id_medico,
        data_consulta=data_consulta,
        observacoes=observacoes
    )

    if resultado == "sucesso":
        flash('Consulta marcada com sucesso!', 'success')
        return redirect(url_for('consulta.listar_consultas'))
    elif resultado == "conflito":
        flash('⚠️ Este horário já está reservado para o médico.', 'warning')
        return redirect(url_for('consulta.nova_consulta'))
    else:
        flash('Erro ao marcar consulta', 'danger')
        return redirect(url_for('consulta.nova_consulta'))



# Editar consulta - GET e POST
@consulta_bp.route('/consultas/editar/<int:id>', methods=['GET', 'POST'])
def editar_consulta(id):
    consulta = facade.buscar_consulta_por_id(id)
    if not consulta:
        flash('Consulta não encontrada', 'danger')
        return redirect(url_for('consulta.listar_consultas'))

    pacientes = facade.listar_pacientes()
    medicos = facade.listar_medicos()

    if request.method == 'POST':
        consulta.id_paciente = request.form.get('id_paciente')
        consulta.id_medico = request.form.get('id_medico')
        consulta.data_consulta = request.form.get('data_consulta')
        consulta.observacoes = request.form.get('observacoes')

        atualizado = facade.atualizar_consulta(
            id=consulta.id,
            id_paciente=consulta.id_paciente,
            id_medico=consulta.id_medico,
            data_consulta=consulta.data_consulta,
            observacoes=consulta.observacoes
        )

        if atualizado:
            flash('Consulta atualizada com sucesso!', 'success')
            return redirect(url_for('consulta.listar_consultas'))
        else:
            flash('Erro ao atualizar consulta', 'danger')

    return render_template('consultas/editar_consulta.html', consulta=consulta, pacientes=pacientes, medicos=medicos)


@consulta_bp.route('/consultas/deletar/<int:id>', methods=['GET', 'POST'])
def deletar_consulta(id):
    consulta = facade.buscar_consulta_por_id(id)
    if not consulta:
        flash('Consulta não encontrada', 'danger')
        return redirect(url_for('consulta.listar_consultas'))

    if request.method == 'POST':
        forcar = request.form.get('forcar') == '1'  # Vem do botão "Excluir mesmo assim"
        resultado = facade.deletar_consulta(id, forcar=forcar)

        if resultado is True:
            flash('Consulta deletada com sucesso!', 'success')
            return redirect(url_for('consulta.listar_consultas'))
        elif "possui pagamento registrado" in resultado:
            # Renderiza nova página de confirmação extra
            return render_template('consultas/confirmar_delete_pagamento.html', consulta=consulta, mensagem=resultado)
        else:
            flash(resultado, 'danger')
            return redirect(url_for('consulta.listar_consultas'))

    return render_template('consultas/confirmar_delete_consulta.html', consulta=consulta)
