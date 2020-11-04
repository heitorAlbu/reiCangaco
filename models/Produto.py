class Produto():
    def __init__(self, nome, preco, descricao, unid):
        self._nome = nome
        self._preco = preco
        self._descricao = descricao
        self._unid = unid

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, preco):
        self._preco = preco

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao
    
    @property
    def unid(self):
        return self._unid

    @unid.setter
    def unid(self, unid):
        self._unid = unid