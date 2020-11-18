from flask import Flask, render_template, request,  session, flash, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from models.Produto import Produto


app = Flask(__name__)
app.secret_key = 'reiDoCangaco'
#engine = create_engine('mysql://root:12345@localhost/db_rei')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.master' 
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    cpf = db.Column(db.String(11), nullable=False)
    tipo = db.Column(db.Integer, nullable=False)

    

    def __str__(self):
        return self.nome

db.create_all()

if __name__ == "__name__":
    app.run(debug=True)



@app.route('/usuarioList')
def usuarioList():
    #if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #return redirect(url_for('login', proxima=url_for('produtoForm')))

    usuarios = Usuario.query.all()
    return render_template('usuarioList.html', usuarios = usuarios)


@app.route('/usuario/delete/<int:id>')
def usuarioDelete(id):
    usuario = Usuario.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    usuarios = Usuario.query.all()
    return redirect(url_for('usuarioList'))

@app.route('/usuario/update/<int:id>')
def usuarioUpdate(id):
    usuario = Usuario.query.filter_by(id=id).first()
    return render_template('usuarioForm.html', usuario = usuario)

@app.route('/produtoForm')
def produtoForm():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('produtoForm')))
    return render_template('produtoForm.html', titulo='Novo Produto')

#@app.route('/criar', methods=['POST',])
#def criar():
    #if 'usuario_logado' not in session or session['usuario_logado'] == None:
    #    return redirect(url_for('login', proxima=url_for('produtoForm')))

    #nome = request.form['nome']
    #preco = request.form['preco']
    #descricao = request.form['descricao']
    # unid = request.form['unid']
    #produto = Produto(nome,preco, descricao, unid)

@app.route('/produtoList')
def produtoList():
    produto = Produto.query.filter_by(id=id).first()
    return render_template('produtoList.html', usuarios = usuarios)

@app.route('/produtoUpdate')
def produtoUpdate(id):
    return render_template('produtoForm.html', produto = produto)

@app.route('/')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('produtoForm')))

    return render_template('home.html', titulo='Rei do cangaço')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuarios = Usuario.query.all()
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.login
            flash(usuario.login + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect (proxima_pagina)
    else:
        flash('Login não realizado !')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect (url_for('login'))