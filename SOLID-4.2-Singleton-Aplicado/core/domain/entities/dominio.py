from dataclasses import dataclass

@dataclass
class Categoria:
    id: int
    descricao: str

    def __init__(self, id: int = None, descricao: str = None):
        self.id = id
        self.descricao = descricao

@dataclass
class Produto:
    id: int
    descricao: str
    preco_unitario: float
    quantidade_estoque: int
    categoria: Categoria

    def __init__(self, id: int = None, descricao: str = None, preco_unitario: float = None, quantidade_estoque: int = None, categoria: Categoria = None):
        self.id = id
        self.descricao = descricao
        self.preco_unitario = preco_unitario
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria