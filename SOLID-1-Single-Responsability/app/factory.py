from .services import BD, CategoriaService, ProdutoService
from .repository import CategoriaRepository, ProdutoRepository


class ServiceFactory:
    
    @staticmethod
    def criar_categoria_service():
        """Cria uma instância de CategoriaService com suas dependências
        
        Returns:
            Instância de CategoriaService
        """
        db = BD.conexao_banco()
        categoria_dao = CategoriaRepository(db)
        return CategoriaService(categoria_dao)
    
    @staticmethod
    def criar_produto_service():
        """Cria uma instância de ProdutoService com suas dependências
        
        Returns:
            Instância de ProdutoService
        """
        db = BD.conexao_banco()
        produto_dao = ProdutoRepository(db)
        return ProdutoService(produto_dao)
    
    @staticmethod
    def criar_categoria_repository(db=None):
        """Cria uma instância de CategoriaRepository
        
        Args:
            db: Conexão do banco (opcional, cria nova se não fornecida)
            
        Returns:
            Instância de CategoriaRepository
        """
        if db is None:
            db = BD.conexao_banco()
        return CategoriaRepository(db)
    
    @staticmethod
    def criar_produto_repository(db=None):
        """Cria uma instância de ProdutoRepository
        
        Args:
            db: Conexão do banco (opcional, cria nova se não fornecida)
            
        Returns:
            Instância de ProdutoRepository
        """
        if db is None:
            db = BD.conexao_banco()
        return ProdutoRepository(db)
