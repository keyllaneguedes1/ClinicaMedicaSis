import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-super-secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/clinica_medica'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
