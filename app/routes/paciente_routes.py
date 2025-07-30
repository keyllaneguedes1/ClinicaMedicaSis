from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.facade.clinica_facade import ClinicaFacade
from app.models.paciente import Paciente
from app import db

paciente_bp = Blueprint('paciente', __name__)
facade = ClinicaFacade()

# Rota para listar pacientes e mostrar a página HTML
@paciente_bp.route('/pacientes', methods=['GET'])
def listar_pacientes():
    pacientes = facade.listar_pacientes()

    if request.accept_mimetypes.best == 'application/json' or request.is_json:
        lista = [{
            'id': p.id,
            'nome': p.nome,
            'data_nascimento': p.data_nascimento.isoformat() if p.data_nascimento else None,
            'sexo': p.sexo,
            'telefone': p.telefone,
            'endereco': p.endereco
        } for p in pacientes]
        return jsonify(lista)

    return render_template('pacientes/pacientes.html', pacientes=pacientes)


@paciente_bp.route('/pacientes/novo', methods=['GET'])
def novo_paciente():
    return render_template('pacientes/novo_paciente.html')


@paciente_bp.route('/pacientes/novo', methods=['POST'])
def cadastrar_paciente():
    nome = request.form.get('nome')
    data_nascimento = request.form.get('data_nascimento')
    sexo = request.form.get('sexo')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')

    paciente = facade.cadastrar_paciente(
        nome=nome,
        data_nascimento=data_nascimento,
        sexo=sexo,
        telefone=telefone,
        endereco=endereco
    )

    if paciente:
        flash('Paciente cadastrado com sucesso!', 'success')
        return redirect(url_for('paciente.listar_pacientes'))
    else:
        flash('Erro ao cadastrar paciente', 'danger')
        return redirect(url_for('paciente.novo_paciente'))


@paciente_bp.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        try:
            paciente.nome = request.form.get('nome')
            paciente.data_nascimento = request.form.get('data_nascimento')
            paciente.sexo = request.form.get('sexo')
            paciente.telefone = request.form.get('telefone')
            paciente.endereco = request.form.get('endereco')

            db.session.commit()
            flash('Paciente atualizado com sucesso!', 'success')
            return redirect(url_for('paciente.listar_pacientes'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar paciente: ' + str(e), 'danger')
            return render_template('pacientes/editar_paciente.html', paciente=paciente)

    return render_template('pacientes/editar_paciente.html', paciente=paciente)


@paciente_bp.route('/pacientes/deletar/<int:id>', methods=['GET', 'POST'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        try:
            db.session.delete(paciente)
            db.session.commit()
            flash('Paciente deletado com sucesso!', 'success')
            return redirect(url_for('paciente.listar_pacientes'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar paciente: {e}")
            flash('Erro ao deletar paciente.', 'danger')
            return redirect(url_for('paciente.listar_pacientes'))

    return render_template('pacientes/confirmar_delete.html', paciente=paciente)


# ------------------- APIs -------------------

@paciente_bp.route('/api/pacientes', methods=['GET'])
def listar_pacientes_api():
    pacientes = facade.listar_pacientes()
    lista = [{
        'id': p.id,
        'nome': p.nome,
        'data_nascimento': p.data_nascimento.isoformat() if p.data_nascimento else None,
        'sexo': p.sexo,
        'telefone': p.telefone,
        'endereco': p.endereco
    } for p in pacientes]
    return jsonify(lista)


@paciente_bp.route('/api/pacientes/novo', methods=['POST'])
def cadastrar_paciente_api():
    data = request.json
    paciente = facade.cadastrar_paciente(
        nome=data.get('nome'),
        data_nascimento=data.get('data_nascimento'),
        sexo=data.get('sexo'),
        telefone=data.get('telefone'),
        endereco=data.get('endereco')
    )
    if paciente:
        return jsonify({'mensagem': 'Paciente cadastrado com sucesso!', 'id': paciente.id}), 201
    else:
        return jsonify({'erro': 'Erro ao cadastrar paciente'}), 500


@paciente_bp.route('/api/pacientes/<int:id>', methods=['PUT'])
def atualizar_paciente_api(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'erro': 'Paciente não encontrado'}), 404

    data = request.json
    paciente.nome = data.get('nome', paciente.nome)
    paciente.cpf = data.get('cpf', paciente.cpf)
    paciente.data_nascimento = data.get('data_nascimento', paciente.data_nascimento)
    paciente.sexo = data.get('sexo', paciente.sexo)
    paciente.telefone = data.get('telefone', paciente.telefone)
    paciente.endereco = data.get('endereco', paciente.endereco)

    try:
        db.session.commit()
        return jsonify({'mensagem': 'Paciente atualizado com sucesso'})
    except:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao atualizar paciente'}), 500


@paciente_bp.route('/api/pacientes/<int:id>', methods=['DELETE'])
def deletar_paciente_api(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'erro': 'Paciente não encontrado'}), 404

    try:
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'mensagem': 'Paciente deletado com sucesso'})
    except:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao deletar paciente'}), 500
