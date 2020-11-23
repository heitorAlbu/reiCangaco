from app.models import Usuario, Fornecedor, Venda, Pedido, Produto
from app import db
from datetime import timedelta
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

def init_app(app):
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
            #teste = current_user(usuario.id)
            return redirect(url_for("home"))
        return render_template(url_for("login"))


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect (url_for('login'))