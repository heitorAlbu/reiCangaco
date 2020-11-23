from app import db, login_manager
from flask_login import UserMixin


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