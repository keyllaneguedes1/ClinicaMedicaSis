from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.facade.clinica_facade import ClinicaFacade

relatorio_bp = Blueprint('relatorio', __name__, url_prefix='/relatorios')
facade = ClinicaFacade()

# Página principal de relatórios
@relatorio_bp.route('/', methods=['GET'])
def relatorios_home():
    return render_template('relatorios/index.html')

# Relatório de histórico de um paciente - responde HTML ou JSON conforme Accept
@relatorio_bp.route('/historico-paciente/<int:id>', methods=['GET'])
def historico_paciente(id):
    dados = facade.historico_paciente_procedure(id)
    if request.accept_mimetypes.accept_html:
        return render_template('relatorios/historico_paciente.html', dados=dados)
    else:
        return jsonify(dados)
    

# Formulário para escolher paciente e ver histórico (HTML)
@relatorio_bp.route('/historico-paciente', methods=['GET', 'POST'])
def historico_paciente_form():
    pacientes = facade.listar_pacientes()

    if request.method == 'POST':
        id_paciente = request.form.get('id_paciente')
        return redirect(url_for('relatorio.historico_paciente_abas', id=id_paciente))

    # Para GET, só renderiza o formulário normalmente
    return render_template('relatorios/historico_paciente_form.html', pacientes=pacientes)



# Relatório de consultas por médico (GET: formulário, POST: resultado)
@relatorio_bp.route('/consultas-por-medico', methods=['GET', 'POST'])
def consultas_por_medico():
    if request.method == 'POST':
        id_medico = request.form.get('id_medico')
        inicio = request.form.get('inicio')  # yyyy-mm-dd
        fim = request.form.get('fim')
        dados = facade.consultas_por_medico_procedure(id_medico, inicio, fim)
        return render_template('relatorios/consultas_por_medico.html', dados=dados)
    medicos = facade.listar_medicos()
    return render_template('relatorios/consultas_por_medico_form.html', medicos=medicos)

# Relatório de todos os históricos dos pacientes (HTML)
@relatorio_bp.route('/historico-pacientes', methods=['GET'])
def historico_pacientes():
    dados = facade.historico_pacientes_view()
    return render_template('relatorios/historico_paciente.html', dados=dados)

# Consultas completas (HTML)
@relatorio_bp.route('/consultas-completas', methods=['GET'])
def consultas_completas():
    dados = facade.consultas_completas_view()
    return render_template('relatorios/consultas_completas.html', dados=dados)

@relatorio_bp.route('/historico-paciente/<int:id>/abas', methods=['GET'])
def historico_paciente_abas(id):
    dados = facade.historico_paciente_procedure(id)
    return render_template('relatorios/historico_paciente_abas.html', dados=dados)

@relatorio_bp.route('/pagamentos', methods=['GET', 'POST'])
def relatorio_pagamentos():
    if request.method == 'POST':
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        relatorio = facade.gerar_relatorio_pagamentos(data_inicio, data_fim)

        if not relatorio:
            flash("Nenhum dado encontrado ou erro ao gerar relatório", "danger")
            return redirect(url_for('relatorio.relatorio_pagamentos'))

        return render_template('relatorios/relatorio_pagamentos_resultado.html',
                               relatorio=relatorio,
                               data_inicio=data_inicio,
                               data_fim=data_fim)
    
    return render_template('relatorios/relatorio_pagamentos.html')

@relatorio_bp.route('/filtro-consultas-periodo', methods=['GET'])
def filtro_consultas_periodo():
    return render_template('relatorios/filtro_consultas_periodo.html')


@relatorio_bp.route('/consultas-periodo', methods=['POST'])
def consultas_por_periodo():
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    consultas = facade.consultas_por_periodo(data_inicio, data_fim)

    return render_template('relatorios/relatorio_consultas_periodo_resultado.html',
                           consultas=consultas,
                           data_inicio=data_inicio,
                           data_fim=data_fim)



