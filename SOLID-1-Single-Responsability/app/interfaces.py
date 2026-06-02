from abc import ABC, abstractmethod


class IConexaoDB(ABC):
    """Interface para gerenciamento de conexão com banco de dados"""
    
    @abstractmethod
    def obter_conexao(self):
        """Retorna uma conexão com o banco de dados"""
        pass


class IDAO(ABC):
    """Interface base para padrão Data Access Object (DAO)"""
    
    @abstractmethod
    def listar_registros(self):
        """Lista todos os registros"""
        pass
    
    @abstractmethod
    def obter_registro(self, id):
        """Obtém um registro pelo ID"""
        pass
    
    @abstractmethod
    def salvar_registro(self, *args, **kwargs):
        """Salva um novo registro"""
        pass
    
    @abstractmethod
    def alterar_registro(self, id, *args, **kwargs):
        """Altera um registro existente"""
        pass
    
    @abstractmethod
    def excluir_registro(self, id):
        """Exclui um registro"""
        pass


class ICategoriaDAO(IDAO):
    """Interface específica para DAO de Categoria"""
    
    @abstractmethod
    def salvar_registro(self, descricao):
        """Salva uma nova categoria"""
        pass
    
    @abstractmethod
    def alterar_registro(self, id, descricao):
        """Altera uma categoria"""
        pass


class IProdutoDAO(IDAO):
    """Interface específica para DAO de Produto"""
    
    @abstractmethod
    def salvar_registro(self, descricao, preco_unitario, quantidade_estoque, categoria_id):
        """Salva um novo produto"""
        pass
    
    @abstractmethod
    def alterar_registro(self, id, descricao, preco_unitario, quantidade_estoque, categoria_id):
        """Altera um produto"""
        pass


class IService(ABC):
    """Interface base para Services (Lógica de Negócio)"""
    
    @abstractmethod
    def listar_registros(self):
        """Lista todos os registros"""
        pass
    
    @abstractmethod
    def obter_registro(self, id):
        """Obtém um registro pelo ID"""
        pass


class ICategoriaService(IService):
    """Interface específica para Service de Categoria"""
    
    @abstractmethod
    def processar_categoria(self, acao, descricao=None, id=None):
        """Processa operação de categoria"""
        pass


class IProdutoService(IService):
    """Interface específica para Service de Produto"""
    
    @abstractmethod
    def processar_produto(self, acao, descricao=None, preco_unitario=None, 
                         quantidade_estoque=None, categoria_id=None, id=None):
        """Processa operação de produto"""
        pass
