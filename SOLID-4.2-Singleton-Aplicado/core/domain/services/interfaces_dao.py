from abc import ABC, abstractmethod
import sqlite3
from typing import Any

from core.domain.entities.dominio import Categoria, Produto


class IConexaoBD(ABC):

    @abstractmethod
    def obter_conexao(self):
        pass

    @abstractmethod
    def executar_comando(self, sql_comando, commit=True) -> Any:
        pass

    @abstractmethod
    def executar_select(self, sql_select) -> list[Any]:
        pass
    

class ICategoriaDAO(ABC):
    
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


class IProdutoDAO(ABC):
    
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
