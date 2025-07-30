from flask import Blueprint, jsonify, request
from app.facade.clinica_facade import ClinicaFacade
from app.models.usuario import Usuario
from app import db

usuario_bp = Blueprint('usuario', __name__)
facade = ClinicaFacade()

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = facade.listar_usuarios()
    return jsonify([u.to_dict() for u in usuarios])

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    usuario = facade.criar_usuario(data)
    return jsonify(usuario.to_dict()), 201


@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify(usuario.to_dict()), 200  

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.json
    usuario = Usuario.query.get_or_404(id)
    for key, value in data.items():
        setattr(usuario, key, value)
    db.session.commit()
    return jsonify(usuario.to_dict()), 200 
 
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário deletado com sucesso.'}), 200
