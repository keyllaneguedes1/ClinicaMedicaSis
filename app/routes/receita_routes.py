from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.receita import Receita

receita_bp = Blueprint('receita', __name__, template_folder='/templates/receitas')

# Listagem HTML
@receita_bp.route('/receitas/html')
def listar_receitas_html():
    receitas = Receita.query.all()
    return render_template('receitas/listar.html', receitas=receitas)

# Formulário de nova receita
@receita_bp.route('/receitas/html/nova', methods=['GET'])
def nova_receita():
    return render_template('receitas/nova.html')

# Criação da receita via formulário
@receita_bp.route('/receitas/html', methods=['POST'])
def criar_receita_html():
    id_consulta = request.form['id_consulta']
    medicamento = request.form['medicamento']
    posologia = request.form['posologia']

    nova = Receita(
        id_consulta=id_consulta,
        medicamento=medicamento,
        posologia=posologia
    )
    db.session.add(nova)
    db.session.commit()
    return redirect(url_for('receita.listar_receitas_html'))

# Formulário para editar
@receita_bp.route('/receitas/html/<int:id>/editar', methods=['GET'])
def editar_receita(id):
    receita = Receita.query.get_or_404(id)
    return render_template('receitas/editar.html', receita=receita)

# Atualizar receita
@receita_bp.route('/receitas/html/<int:id>', methods=['POST'])
def atualizar_receita_html(id):
    receita = Receita.query.get_or_404(id)
    receita.id_consulta = request.form['id_consulta']
    receita.medicamento = request.form['medicamento']
    receita.posologia = request.form['posologia']

    db.session.commit()
    return redirect(url_for('receita.listar_receitas_html'))

# Excluir receita
@receita_bp.route('/receitas/html/<int:id>/excluir', methods=['GET'])
def excluir_receita(id):
    receita = Receita.query.get_or_404(id)
    db.session.delete(receita)
    db.session.commit()
    return redirect(url_for('receita.listar_receitas_html'))
