from abc import ABC, abstractmethod
import sqlite3
from typing import Any

from core.domain.entities.dominio import Categoria, Produto
from core.domain.services.interfaces_dao import ICategoriaDAO, IConexaoBD, IProdutoDAO

from termcolor import colored, cprint


class ConexaoBD(IConexaoBD):

    # variável para armazenar a instância única da classe (singleton)
    __singleton = None

    # método especial __new__ é chamado antes do __init__ e 
    # é responsável por criar a instância da classe
    def __new__(cls):
        
        # se nenhuma instância foi criada ainda, cria uma nova 
        # instância e armazena na variável __singleton
        if cls.__singleton is None:
        
            # cria instância única (singleton)
            cls.__singleton = super().__new__(cls)

            # cria uma conexao com o BD e armazena na instância única (singleton)
            cls.__singleton.__conexao = sqlite3.connect('db_solid.sqlite3')
            
            # comando para não permitir DELETE CASCADE (exclusão em cascata)
            cls.__singleton.__conexao.execute("PRAGMA foreign_keys = ON;") 
        
            # mensagem para debug
            cprint(f'\n ** Conectou ao Banco de Dados ** \n', 
                   "white", "on_light_red", attrs=['bold'])

        # retorna a instância única da conexão com o BD
        return cls.__singleton

    def obter_conexao(self):
        '''Estabelece a conexao com o SQLite usando o padrão Singleton'''
        return self.__singleton.__conexao
    
    def executar_comando(self, sql_comando, commit=True) -> Any:
        '''Executa um comando SQL no BD (geralmente um INSERT, UPDATE ou DELETE)'''
        # obtem conexao
        conexao = self.obter_conexao()
        # cria um cursor() e executa o SQL informado
        ret = conexao.cursor().execute(sql_comando)
        # verifica se eh para efetivar as modificações no BD
        if commit:
            conexao.commit()
        # retorna o resultado da execução do comando SQL
        return ret 

    def executar_select(self, sql_select) -> list[Any]:
        '''Executa um comando SELECT no BD e retorna os registros'''
        # obtem conexao
        conexao = self.obter_conexao()
        # cria um cursor(), executa o SELECT informado e traz os todos os registros
        ret = conexao.cursor().execute(sql_select).fetchall()
        # retorna os registros do BD
        return ret 



class CategoriaDAO(ICategoriaDAO):

    def __init__(self, conexao: IConexaoBD): 
        self._conexao = conexao

    def incluir(self, obj: Categoria) -> Categoria: 
        sql = f"INSERT INTO Categoria(descricao) VALUES('{obj.descricao}')"
        self._conexao.executar_comando(sql)
        return obj

    def alterar(self, obj: Categoria) -> Categoria: 
        sql = f'''  UPDATE Categoria 
                    SET descricao = '{obj.descricao}' 
                    WHERE id = {obj.id}'''        
        self._conexao.executar_comando(sql)
        return obj
    
    def excluir(self, id: int): 
        sql = f"DELETE FROM Categoria WHERE id = {id}"
        self._conexao.executar_comando(sql)
    
    def obter_por_id(self, id: int) -> Categoria: 
        # seleciona o registro pelo id informado
        sql = f'''  SELECT  id, descricao FROM Categoria WHERE id={id} '''
        # executa o select e pega o primeiro registro([0])
        reg = self._conexao.executar_select(sql)[0]
        # converte o registro para objeto e retorna
        return Categoria(id=reg[0], descricao=reg[1])
    
    def listar(self) -> list[Categoria]: 
        # seleciona as categorias
        sql = '''   SELECT  id, descricao FROM Categoria ORDER BY descricao '''
        # obtem todos os registros retornados
        registros = self._conexao.executar_select(sql)
        # converte os registros para objetos e adiciona na lista
        dados = list()
        for reg in registros:
            dados.append( Categoria(id=reg[0], descricao=reg[1]) )
        # retorna
        return dados




class ProdutoDAO(IProdutoDAO):

    def __init__(self, conexao: IConexaoBD): 
        self._conexao = conexao

    def incluir(self, obj: Produto) -> Produto: 
        sql = f'''
            INSERT INTO Produto (
                descricao, 
                preco_unitario, 
                quantidade_estoque, 
                categoria_id
            )
            VALUES(
                '{obj.descricao}', 
                {obj.preco_unitario}, 
                {obj.quantidade_estoque}, 
                {obj.categoria.id}
            );
        '''
        self._conexao.executar_comando(sql)
        return obj

    def alterar(self, obj: Produto) -> Produto: 
        sql = f''' 
            UPDATE Produto
            SET descricao          = '{obj.descricao}', 
                preco_unitario     = {obj.preco_unitario}, 
                quantidade_estoque = {obj.quantidade_estoque}, 
                categoria_id       = {obj.categoria.id}
            WHERE id = {obj.id};
        '''
        self._conexao.executar_comando(sql)
        return obj
    
    def excluir(self, id: int): 
        sql = f"DELETE FROM Produto WHERE id = {id}"
        self._conexao.executar_comando(sql)

    def obter_por_id(self, id: int) -> Produto: 
        # seleciona o registro pelo id informado
        sql = f'''
            SELECT  pro.id,
                    pro.descricao, 
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as 'categoria_descricao'
                    
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id

            WHERE pro.id={id}    
        '''
        # executa o select e pega o primeiro registro([0])
        reg = self._conexao.executar_select(sql)[0]

        # converte o registro para objeto e retorna
        prod = Produto(
            id=reg[0], 
            descricao=reg[1],
            preco_unitario=reg[2],
            quantidade_estoque=reg[3],
            categoria=Categoria(id=reg[4], descricao=reg[5]),
        ) 
        # retorna o objeto Produto
        return prod
    

    def listar(self) -> list[Produto]: 
        # seleciona os produtos
        sql = '''
            SELECT  pro.id,
                    pro.descricao, 
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as 'categoria_descricao'
                    
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id

            ORDER BY pro.descricao
        '''
        # obtem todos os registros retornados
        registros = self._conexao.executar_select(sql)
        # converte os registros para objetos e adiciona na lista
        dados = list()
        for reg in registros:
            # cria objeto Produto
            prod = Produto(
                id=reg[0], 
                descricao=reg[1],
                preco_unitario=reg[2],
                quantidade_estoque=reg[3],
                categoria=Categoria(id=reg[4], descricao=reg[5]),
            ) 
            # adiciona na lista de retorno 
            dados.append(prod)
        # retorna
        return dados
