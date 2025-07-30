from flask import Flask
from config import Config

from app.extensions import db  # <-- Importa de outro lugar

from app.routes.paciente_routes import paciente_bp
from app.routes.medicos_routes import medico_bp
from app.routes.consulta_routes import consulta_bp
from app.routes.exame_routes import exame_bp
from app.routes.receita_routes import receita_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.relatorio import relatorio_bp
from app.routes.index import index_bp
from app.routes.pagamento_routes import pagamento_bp
from app.models import register_models
from datetime import datetime
import pytz

def utc_to_local(value, fmt='%d/%m/%Y %H:%M'):
    if value is None:
        return ''
    if not isinstance(value, datetime):
        return value

    utc = pytz.utc
    local_tz = pytz.timezone("America/Sao_Paulo")

    utc_dt = utc.localize(value) if value.tzinfo is None else value
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt.strftime(fmt)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.jinja_env.filters['utc_to_local'] = utc_to_local

    db.init_app(app)

    register_models()  # Isso agora funciona

    app.register_blueprint(exame_bp)
    app.register_blueprint(receita_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(medico_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(relatorio_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(pagamento_bp)

    return app
