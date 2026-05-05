import sqlite3

class BD():

    @staticmethod
    def conexao_banco():
        conexao = sqlite3.connect('db_solid.sqlite3')
            # comando para não permitir DELETE CASCADE (exclusão em cascata)
        conexao.execute("PRAGMA foreign_keys = ON;") 
            # Método responsavel por listar, incluir, alterar e excluir as Categorias.
        return conexao
    
    @staticmethod
    def listar_registros():
        conexao = BD.conexao_banco()
        sql = '''
                SELECT  id, 
                        descricao
                FROM Categoria 
                ORDER BY descricao
            '''
        registros = conexao.cursor().execute(sql).fetchall()
            # cria um cursor(), executa o SELECT informado e traz os todos os registros
        return registros