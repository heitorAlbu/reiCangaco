from flask import Flask, render_template, request,  session, flash, url_for,redirect

app = Flask(__name__)
app.secret_key = 'reiDoCangaco'

class Usuario:
    def __init__(self,  login, senha):
        self.login = login
        self.senha = senha

usuario1 = Usuario('heitor','12345')
usuario2 = Usuario('ricardo','54321')
usuarios = { usuario1.login: usuario1, 
             usuario2.login: usuario2}

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
    return render_template('produtoList.html')

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