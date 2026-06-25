from abc import ABC, abstractmethod

from core.domain.entities.dominio import Categoria, Produto
from core.domain.services.interfaces_dao import ICategoriaDAO, IProdutoDAO


class ICategoriaService(ABC):

    @abstractmethod
    def validar(self, obj: Categoria): 
        pass

    @abstractmethod
    def incluir(self, obj: Categoria) -> Categoria: 
        pass

    @abstractmethod
    def alterar(self, obj: Categoria) -> Categoria: 
        pass

    @abstractmethod
    def excluir(self, id: int): 
        pass        

    @abstractmethod
    def obter_por_id(self, id: int) -> Categoria: 
        pass

    @abstractmethod
    def listar(self) -> list[Categoria]: 
        pass


class IProdutoService(ABC):

    @abstractmethod
    def validar(self, obj: Produto): 
        pass

    @abstractmethod
    def incluir(self, obj: Produto) -> Produto: 
        pass

    @abstractmethod
    def alterar(self, obj: Produto) -> Produto: 
        pass

    @abstractmethod
    def excluir(self, id: int): 
        pass        

    @abstractmethod
    def obter_por_id(self, id: int) -> Produto: 
        pass

    @abstractmethod
    def listar(self) -> list[Produto]: 
        pass
