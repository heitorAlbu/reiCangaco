from flask import Flask, render_template, request,  session, flash, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from models.Produto import Produto
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.secret_key = 'reiDoCangaco'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.master' 
db = SQLAlchemy(app)
login_manager = LoginManager(app)


venda_produto = db.Table('venda_produto',
    db.Column('venda_id', db.Integer, db.ForeignKey('venda.id')),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'))
)

pedido_produto = db.Table('pedido_produto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'))
)

@login_manager.user_loader
def current_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    tipoPessoa = db.Column(db.String(2), nullable=False)
    cpf = db.Column(db.String(11), nullable=True)
    tipoUsuario = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.nome

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=True)
    cpf = db.Column(db.String(11), nullable=True)
    produtos = db.relationship('Produto', backref='fornecedor_produto')
    pedidos = db.relationship('Pedido', backref='fornecedor_pedido')
    
    def __str__(self):
        return self.nome        

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    unidVenda = db.Column(db.String(15), nullable=True)
    fornecedor_produto_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))

    def __str__(self):
        return self.nome

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime ,nullable=False)
    total = db.Column(db.Float, nullable=False)
    produtos = db.relationship('Produto', secondary=venda_produto, backref=db.backref('venda_produto', lazy='dynamic'))

    def __str__(self):
        return self.id

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime ,nullable=False)
    total = db.Column(db.Float, nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    produtos = db.relationship('Produto', secondary=pedido_produto, backref=db.backref('pedido_produto', lazy='dynamic'))
    
    def __str__(self):
        return self.id

#db.create_all()

if __name__ == "__name__":
    app.run(debug=True)

@app.route('/usuarioList')
def usuarioList():
    usuarios = Usuario.query.all()
    return render_template('usuarioList.html', usuarios = usuarios)

@app.route('/usuarioRegister', methods=["GET", "POST"])
def usuarioRegister():
  
    if request.method == "POST":
        usuario = Usuario()
        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        usuario.senha = request.form["senha"]
        usuario.endereco = request.form["endereco"]
        usuario.telefone = request.form["telefone"]
        usuario.cpf = request.form["cpf"]
        usuario.tipoUsuario = request.form["tipo"]
        usuario.tipoPessoa = "PF"

        db.session.add(usuario)
        db.session.commit()
        usuarios = Usuario.query.all()
        return render_template("usuarioList.html", usuarios = usuarios)
    else:
        usuario = Usuario()
        return render_template('usuarioForm.html', usuario=usuario)

@app.route('/usuario/delete/<int:id>')
def usuarioDelete(id):
    usuario = Usuario.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    usuarios = Usuario.query.all()
    return redirect(url_for('usuarioList'))

@app.route('/usuarioUpdate/<int:id>', methods=["GET", "POST"])
def usuarioUpdate(id):
    if request.method == "GET":
        usuario = Usuario.query.filter_by(id=id).first()
        return render_template('usuarioUpdate.html', usuario = usuario)
    if request.method == "POST":
        Id = request.form["id_usuario"]
        
        usuario = Usuario.query.filter_by(id=int(Id)).first()
        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        usuario.senha = request.form["senha"]
        usuario.endereco = request.form["endereco"]
        usuario.telefone = request.form["telefone"]
        usuario.cpf = request.form["cpf"]
        usuario.tipoUsuario = request.form["tipo"]
        usuario.tipoPessoa = "PF"

        db.session.commit()
        usuarios = Usuario.query.all()

        return render_template('usuarioList.html', usuarios = usuarios)


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
    return render_template('produtoList.html', produto = produtolista)

@app.route('/produtoUpdate')
def produtoUpdate(id):
    return render_template('produtoForm.html', produto = produtolista)

@app.route('/')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('produtoForm')))

    return render_template('home.html', titulo='Rei do cangaço')




@app.route('/login', methods=["GET","POST"])
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