from flask import Flask, render_template, request,  session, flash, url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models.Produto import Produto
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#app.secret_key = 'reiDoCangaco'
app.config["SECRET_KEY"] = 'secret'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.master' 
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def current_user(user_id):
    return Usuario.query.get(user_id)

venda_produto = db.Table('venda_produto',
    db.Column('venda_id', db.Integer, db.ForeignKey('venda.id')),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'))
)

pedido_produto = db.Table('pedido_produto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'))
)

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


############# [ USUARIO ] #############################
@app.route('/usuarioForm')
@login_required
def usuarioForm():
    return render_template('usuarioForm.html')

@app.route('/usuarioList')
@login_required
def usuarioList():
    usuarios = Usuario.query.all()
    return render_template('usuarioList.html', usuarios = usuarios)

@app.route('/usuarioRegister', methods=["GET", "POST"])
def usuarioRegister():
  
    if request.method == "POST":
        usuario = Usuario()
        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        usuario.senha = generate_password_hash(request.form["senha"])
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
@login_required
def usuarioDelete(id):
    usuario = Usuario.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    usuarios = Usuario.query.all()
    return redirect(url_for('usuarioList'))

@app.route('/usuarioUpdate/<int:id>', methods=["GET", "POST"])
@login_required
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

############# [ PRODUTO ] #############################

@app.route('/produtoForm')
@login_required
def produtoForm():
    fornecedores = Fornecedor.query.all()
    return render_template('produtoForm.html', titulo='Novo Produto', fornecedores=fornecedores)


@app.route('/produtoList')
def produtoList():
    produtos = Produto.query.all()
    return render_template('produtoList.html', produtos = produtos)

@app.route('/produtoRegister', methods=["GET", "POST"])
def produtoRegister():
    if request.method == "POST":
        produto = Produto()
        produto.nome = request.form["nome"]
        produto.descricao = request.form["descricao"]
        produto.preco = request.form["preco"]
        produto.unidVenda = request.form["unidVenda"]
        produto.fornecedor_produto_id = request.form["listafornecedores"]
        
        db.session.add(produto)
        db.session.commit()
        produtos = Produto.query.all()
        return render_template('produtoList.html', produtos = produtos)
    else:
        produto = Produto()
        return render_template('produtoForm.html', produto = produto)

@app.route('/produto/delete/<int:id>')
@login_required
def produtoDelete(id):
    produto = Produto.query.filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    produtos = Produto.query.all()
    return redirect(url_for('produtoList'))

@app.route('/produtoUpdate/<int:id>', methods=["GET", "POST"])
@login_required
def produtoUpdate(id):
    if request.method == "GET":
        produto = Produto.query.filter_by(id=id).first()
        return render_template('produtoUpdate.html', produto = produto)
    if request.method == "POST":
        Id = request.form["id_produto"]
        produto = Produto.query.filter_by(id=int(Id)).first()
        produto.nome = request.form["nome"]
        produto.descricao = request.form["descricao"]
        produto.preco = request.form["preco"]
        produto.unidVenda = request.form["unidVenda"] 
        db.session.commit()
        produtos = Produto.query.all()
        return render_template('produtoList.html', produtos = produtos)

############# [ VENDA ] #############################

@app.route('/vendaList')
@login_required
def vendaList():
    return render_template('home.html')

############# [ FORNECEDOR ] #############################

@app.route('/fornecedorForm')
def fornecedorForm():
    return render_template('fornecedorForm.html')

@app.route('/fornecedorList')
@login_required
def fornecedorList():
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedorList.html', fornecedores = fornecedores)

@app.route('/fornecedorUpdate/<int:id>', methods=["GET", "POST"])
@login_required
def fornecedorUpdate(id):
    if request.method == "GET":
        fornecedor = Fornecedor.query.filter_by(id=id).first()
        return render_template('fornecedorUpdate.html', fornecedor=fornecedor)
    if request.method == "POST":
        Id = request.form["id_fornecedor"]
        fornecedor = Fornecedor.query.filter_by(id=int(Id)).first()
        fornecedor.nome = request.form["nome"]
        fornecedor.nickname = request.form["nickname"]
        fornecedor.cpf = request.form["cpf"]
        fornecedor.cnpj = request.form["cnpj"]

        db.session.commit()
        fornecedores = Fornecedor.query.all()

        return render_template('fornecedorList.html', fornecedores = fornecedores)


@app.route('/fornecedor/delete/<int:id>')
@login_required
def fornecedorDelete(id):
    fornecedor = Fornecedor.query.filter_by(id=id).first()
    db.session.delete(fornecedor)
    db.session.commit()
    fornecedores = Fornecedor.query.all()
    return redirect(url_for('fornecedorList'))

@app.route('/fornecedorRegister', methods=["GET", "POST"])
def fornecedorRegister():
    if request.method == "POST":
        fornecedor = Fornecedor()
        fornecedor.nome = request.form["nome"]
        fornecedor.nickname = request.form["nickname"]
        fornecedor.cpf = request.form["cpf"]
        fornecedor.cnpj = request.form["cnpj"]

        db.session.add(fornecedor)
        db.session.commit()
        fornecedores = Fornecedor.query.all()
        return render_template("fornecedorList.html", fornecedores = fornecedores)
    else:
        fornecedor = Fornecedor()
        return render_template('fornecedorForm.html', fornecedor=fornecedor)

#############{HOME E LOGIN}
@app.route('/')
@login_required
def home():
    return render_template('home.html', titulo='Rei do cangaço', image_file = url_for('static', filename="usricon.jpg"))

@app.route('/login', methods=["GET","POST"])
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima , image_file = url_for('static', filename="loginbg.png"))

@app.route('/autenticar', methods=["GET","POST"])
def autenticar():
    proxima_pagina = request.form['proxima']
    if request.method=="POST":
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email = email).first()

        if not usuario:
            flash("Credenciais inválidas")
            return redirect(url_for("login"))
        if not check_password_hash(usuario.senha , senha):
            flash("Credenciais inválidas")
            return redirect(url_for("login"))
        login_user(usuario)
        teste = current_user(usuario.id)
        return redirect(url_for("home"))

    return render_template(url_for("login"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect (url_for('login'))