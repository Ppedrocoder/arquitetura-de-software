from .interfaces import ICategoriaDAO, IProdutoDAO


class CategoriaRepository(ICategoriaDAO):
    
    def __init__(self, db):
        """Inicializa repository com conexão ao banco de dados
        
        Args:
            db: Conexão com o banco de dados (injeção de dependência)
        """
        self.db = db

    def listar_registros(self):
        """Lista todas as categorias"""
        sql = '''
            SELECT id, 
                   descricao
            FROM Categoria 
            ORDER BY descricao
        '''
        registros = self.db.cursor().execute(sql).fetchall()
        return registros

    def obter_registro(self, id):
        """Obtém uma categoria por ID"""
        sql = '''
            SELECT id, 
                   descricao
            FROM Categoria 
            WHERE id = ?
        '''
        registro = self.db.cursor().execute(sql, (id,)).fetchone()
        return registro

    def salvar_registro(self, descricao):
        """Insere uma nova categoria"""
        sql = 'INSERT INTO Categoria(descricao) VALUES(?)'
        self.db.cursor().execute(sql, (descricao,))
        self.db.commit()
        return self.db.cursor().lastrowid

    def alterar_registro(self, id, descricao):
        """Atualiza uma categoria existente"""
        sql = 'UPDATE Categoria SET descricao = ? WHERE id = ?'
        self.db.cursor().execute(sql, (descricao, id))
        self.db.commit()
        return self.db.cursor().rowcount

    def excluir_registro(self, id):
        """Deleta uma categoria"""
        sql = 'DELETE FROM Categoria WHERE id = ?'
        self.db.cursor().execute(sql, (id,))
        self.db.commit()
        return self.db.cursor().rowcount 


class ProdutoRepository(IProdutoDAO):
    
    def __init__(self, db):
        """Inicializa repository com conexão ao banco de dados
        
        Args:
            db: Conexão com o banco de dados (injeção de dependência)
        """
        self.db = db

    def listar_registros(self):
        """Lista todos os produtos com suas categorias"""
        sql = '''
            SELECT pro.id,
                   pro.descricao, 
                   pro.preco_unitario,
                   pro.quantidade_estoque,
                   pro.categoria_id,
                   cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            ORDER BY pro.descricao
        '''
        registros = self.db.cursor().execute(sql).fetchall()
        return registros

    def obter_registro(self, id):
        """Obtém um produto por ID com sua categoria"""
        sql = '''
            SELECT p.id, 
                   p.descricao, 
                   p.preco_unitario, 
                   p.quantidade_estoque, 
                   c.id as categoria_id,
                   c.descricao as categoria
            FROM Produto p
            INNER JOIN Categoria c ON c.id = p.categoria_id
            WHERE p.id = ?
        '''
        registro = self.db.cursor().execute(sql, (id,)).fetchone()
        return registro

    def salvar_registro(self, descricao, preco_unitario, quantidade_estoque, categoria_id):
        """Insere um novo produto"""
        sql = '''
            INSERT INTO Produto (
                descricao, 
                preco_unitario, 
                quantidade_estoque, 
                categoria_id
            ) VALUES(?, ?, ?, ?)
        '''
        self.db.cursor().execute(sql, (descricao, preco_unitario, quantidade_estoque, categoria_id))
        self.db.commit()
        return self.db.cursor().lastrowid

    def alterar_registro(self, id, descricao, preco_unitario, quantidade_estoque, categoria_id):
        """Atualiza um produto existente"""
        sql = '''
            UPDATE Produto 
            SET descricao = ?, 
                preco_unitario = ?, 
                quantidade_estoque = ?, 
                categoria_id = ? 
            WHERE id = ?
        '''
        self.db.cursor().execute(sql, (descricao, preco_unitario, quantidade_estoque, categoria_id, id))
        self.db.commit()
        return self.db.cursor().rowcount

    def excluir_registro(self, id):
        """Deleta um produto"""
        sql = 'DELETE FROM Produto WHERE id = ?'
        self.db.cursor().execute(sql, (id,))
        self.db.commit()
        return self.db.cursor().rowcount