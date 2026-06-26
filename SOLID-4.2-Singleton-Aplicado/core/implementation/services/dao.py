from abc import ABC, abstractmethod
import sqlite3
from typing import Any

from core.domain.entities.dominio import Categoria, Produto
from core.domain.services.interfaces_dao import ICategoriaDAO, IConexaoBD, IProdutoDAO

from termcolor import colored, cprint


class ConexaoBD(IConexaoBD):

    MAX_CONEXOES = 5
 
    _pool: list["ConexaoBD"] = []
    _contador = 0

    # método especial __new__ é chamado antes do __init__ e 
    # é responsável por criar a instância da classe
    def __new__(cls):
 
        # enquanto não atingiu o limite, cria novas instâncias
        if len(cls._pool) < cls.MAX_CONEXOES:
 
            instancia = super().__new__(cls)
            instancia._conexao = sqlite3.connect('db_solid.sqlite3', check_same_thread=False)
            instancia._conexao.execute("PRAGMA foreign_keys = ON;")
            instancia._id = len(cls._pool) + 1
 
            cls._pool.append(instancia)
 
            cprint(
                f'\n ** Conectou ao BD — nova instância criada: #{instancia._id} de {cls.MAX_CONEXOES} ** \n',
                "white", "on_light_red", attrs=['bold']
            )
 
        else:
            # pool cheio: reutiliza as instâncias já criadas
            idx = cls._contador % cls.MAX_CONEXOES
            cls._contador += 1
            instancia = cls._pool[idx]
 
            cprint(
                f'\n ** Conectou ao BD — utilizando instância #{instancia._id} de {cls.MAX_CONEXOES} ** \n',
                "white", "on_light_red", attrs=['bold']
            )
 
        return instancia

    def obter_conexao(self):
        '''Estabelece a conexao com o SQLite usando o padrão Singleton'''
        return self._conexao
    
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
