from flask import Flask, render_template, request, redirect, url_for
from models import db, Aluno, Maquina
from client_control import bloquear_maquina, liberar_maquina

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerenciador.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    alunos = Aluno.query.all()
    maquinas = Maquina.query.all()
    return render_template('index.html', alunos=alunos, maquinas=maquinas)

@app.route('/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():
    nome = request.form['nome']
    matricula = request.form['matricula']
    novo = Aluno(nome=nome, matricula=matricula)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar_tempo/<int:aluno_id>', methods=['POST'])
def editar_tempo(aluno_id):
    novo_tempo = int(request.form['tempo'])
    aluno = Aluno.query.get(aluno_id)
    if aluno:
        aluno.tempo_restante = novo_tempo
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/desvincular/<int:maquina_id>')
def desvincular(maquina_id):
    maquina = Maquina.query.get(maquina_id)
    if maquina:
        maquina.aluno = None
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/cadastrar_maquina', methods=['POST'])
def cadastrar_maquina():
    ip = request.form['ip']
    nova = Maquina(ip=ip)
    db.session.add(nova)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/vincular', methods=['POST'])
def vincular():
    aluno_id = int(request.form['aluno_id'])
    maquina_id = int(request.form['maquina_id'])
    aluno = Aluno.query.get(aluno_id)
    maquina = Maquina.query.get(maquina_id)
    maquina.aluno = aluno
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/usar/<int:maquina_id>/<int:tempo>')
def usar_maquina(maquina_id, tempo):
    maquina = Maquina.query.get(maquina_id)
    if maquina and maquina.aluno:
        aluno = maquina.aluno
        if aluno.tempo_restante >= tempo:
            aluno.tempo_restante -= tempo
            db.session.commit()
            liberar_maquina(maquina.ip)
    return redirect(url_for('index'))

@app.route('/bloquear/<int:maquina_id>')
def bloquear(maquina_id):
    maquina = Maquina.query.get(maquina_id)
    if maquina:
        bloquear_maquina(maquina.ip)
    return redirect(url_for('index'))

@app.route('/liberar/<int:maquina_id>')
def liberar(maquina_id):
    maquina = Maquina.query.get(maquina_id)
    if maquina:
        liberar_maquina(maquina.ip)
    return redirect(url_for('index'))

@app.route('/resetar/<int:aluno_id>')
def resetar(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if aluno:
        aluno.tempo_restante = 160
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
