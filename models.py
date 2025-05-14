from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    matricula = db.Column(db.String(50), unique=True)
    tempo_restante = db.Column(db.Integer, default=160)
    maquinas = db.relationship('Maquina', backref='aluno')

class Maquina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100), unique=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))
