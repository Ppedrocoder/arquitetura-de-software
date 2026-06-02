import sqlite3
from .interfaces import ICategoriaService, IProdutoService, ICategoriaDAO, IProdutoDAO


class BD:
    
    @staticmethod
    def conexao_banco():
        """Cria e retorna uma conexão com o banco de dados
        
        Returns:
            Conexão sqlite3 configurada
        """
        conexao = sqlite3.connect('db_solid.sqlite3')
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao


class CategoriaService(ICategoriaService):
    
    def __init__(self, repository: ICategoriaDAO):
        """Inicializa o service com um repository
        
        Args:
            repository: Instância que implementa ICategoriaDAO (injeção de dependência)
        """
        self.repository = repository
    
    def listar_registros(self):
        """
        Lista todas as categorias
        
        Returns:
            Lista de categorias
        """
        try:
            return self.repository.listar_registros()
        except Exception as e:
            raise Exception(f"Erro ao listar categorias: {str(e)}")
    
    def obter_registro(self, id):
        """
        Obtém uma categoria por ID
        
        Args:
            id: ID da categoria
            
        Returns:
            Tupla com (id, descricao) ou None
        """
        try:
            id = int(id)
            if not id or id <= 0:
                raise ValueError("ID deve ser um número válido")
            
            registro = self.repository.obter_registro(id)
            if not registro:
                raise ValueError(f"Categoria com ID {id} não encontrada")
            
            return registro
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao obter categoria: {str(e)}")
    
    def salvar_categoria(self, descricao):
        """
        Salva uma nova categoria
        
        Args:
            descricao: Descrição da categoria
            
        Returns:
            ID da categoria criada
        """
        try:
            if not descricao or len(descricao.strip()) == 0:
                raise ValueError("Descrição não pode estar vazia")

            descricao = descricao.strip()
            if len(descricao) > 30:
                raise ValueError("Descrição não pode ter mais de 30 caracteres")

            return self.repository.salvar_registro(descricao)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao salvar categoria: {str(e)}")
    
    def alterar_categoria(self, id, descricao):
        """
        Altera uma categoria existente
        
        Args:
            id: ID da categoria
            descricao: Nova descrição
            
        Returns:
            Número de registros alterados
        """
        try:
            id = int(id)
            if not id or id <= 0:
                raise ValueError("ID deve ser um número válido")

            if not descricao or len(descricao.strip()) == 0:
                raise ValueError("Descrição não pode estar vazia")

            descricao = descricao.strip()
            if len(descricao) > 30:
                raise ValueError("Descrição não pode ter mais de 30 caracteres")

            if not self.repository.obter_registro(id):
                raise ValueError(f"Categoria com ID {id} não encontrada")

            return self.repository.alterar_registro(id, descricao)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao alterar categoria: {str(e)}")
    
    def excluir_categoria(self, id):
        """
        Exclui uma categoria
        
        Args:
            id: ID da categoria
            
        Returns:
            Número de registros deletados
        """
        try:
            id = int(id)
            if not id or id <= 0:
                raise ValueError("ID deve ser um número válido")

            if not self.repository.obter_registro(id):
                raise ValueError(f"Categoria com ID {id} não encontrada")

            return self.repository.excluir_registro(id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao excluir categoria: {str(e)}")
    
    def processar_categoria(self, acao, descricao=None, id=None):
        """
        Roteia a operação de categoria baseado na ação
        Responsabilidade da service: decidir qual método executar
        
        Args:
            acao: Tipo de ação ('Inclusão', 'Alteração', 'Exclusão')
            descricao: Descrição da categoria (obrigatória para Inclusão/Alteração)
            id: ID da categoria (obrigatória para Alteração/Exclusão)
            
        Returns:
            Resultado da operação
        """
        if acao == 'Exclusão':
            return self.excluir_categoria(id)
        elif acao == 'Alteração':
            return self.alterar_categoria(id, descricao)
        else: 
            return self.salvar_categoria(descricao)


class ProdutoService(IProdutoService):
    
    def __init__(self, repository: IProdutoDAO):
        """Inicializa o service com um repository
        
        Args:
            repository: Instância que implementa IProdutoDAO (injeção de dependência)
        """
        self.repository = repository
    
    def listar_registros(self):
        """
        Lista todos os produtos
        
        Returns:
            Lista de produtos com categorias
        """
        try:
            return self.repository.listar_registros()
        except Exception as e:
            raise Exception(f"Erro ao listar produtos: {str(e)}")
    
    def obter_registro(self, id):
        """
        Obtém um produto por ID
        
        Args:
            id: ID do produto
            
        Returns:
            Tupla com dados do produto ou None
        """
        try:
            id = int(id)
            if not id or id <= 0:
                raise ValueError("ID deve ser um número válido")
            
            registro = self.repository.obter_registro(id)
            if not registro:
                raise ValueError(f"Produto com ID {id} não encontrado")
            
            return registro
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao obter produto: {str(e)}")
    
    def salvar_produto(self, descricao, preco_unitario, quantidade_estoque, categoria_id):
        """
        Salva um novo produto
        
        Args:
            descricao: Descrição do produto
            preco_unitario: Preço unitário
            quantidade_estoque: Quantidade em estoque
            categoria_id: ID da categoria
            
        Returns:
            ID do produto criado
        """
        try:
            if not descricao or len(descricao.strip()) == 0:
                raise ValueError("Descrição não pode estar vazia")
            
            descricao = descricao.strip()
            
            if len(descricao) > 50:
                raise ValueError("Descrição não pode ter mais de 50 caracteres")
            
            try:
                preco_unitario = float(preco_unitario)
                quantidade_estoque = int(quantidade_estoque)
                categoria_id = int(categoria_id)
            except (ValueError, TypeError):
                raise ValueError("Preço deve ser número, estoque e categoria devem ser inteiros")
            
            if preco_unitario < 0:
                raise ValueError("Preço não pode ser negativo")
            
            if quantidade_estoque < 0:
                raise ValueError("Estoque não pode ser negativo")
            
            if categoria_id <= 0:
                raise ValueError("Categoria inválida")
            
            return self.repository.salvar_registro(descricao, preco_unitario, quantidade_estoque, categoria_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao salvar produto: {str(e)}")
    
    def alterar_produto(self, id, descricao, preco_unitario, quantidade_estoque, categoria_id):
        """
        Altera um produto existente
        
        Args:
            id: ID do produto
            descricao: Nova descrição
            preco_unitario: Novo preço
            quantidade_estoque: Novo estoque
            categoria_id: Nova categoria
            
        Returns:
            Número de registros alterados
        """
        try:
            id = int(id)
            if not id or id <= 0:
                raise ValueError("ID deve ser um número válido")
            
            descricao = descricao.strip()
            
            if len(descricao) > 50:
                raise ValueError("Descrição não pode ter mais de 50 caracteres")
            
            try:
                preco_unitario = float(preco_unitario)
                quantidade_estoque = int(quantidade_estoque)
                categoria_id = int(categoria_id)
            except (ValueError, TypeError):
                raise ValueError("Preço deve ser número, estoque e categoria devem ser inteiros")
            
            if preco_unitario < 0:
                raise ValueError("Preço não pode ser negativo")
            
            if quantidade_estoque < 0:
                raise ValueError("Estoque não pode ser negativo")
            
            if categoria_id <= 0:
                raise ValueError("Categoria inválida")
            
            if not self.repository.obter_registro(id):
                raise ValueError(f"Produto com ID {id} não encontrado")
            
            return self.repository.alterar_registro(id, descricao, preco_unitario, quantidade_estoque, categoria_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao alterar produto: {str(e)}")
    
    def excluir_produto(self, id):
        """
        Exclui um produto
        
        Args:
            id: ID do produto
            
        Returns:
            Número de registros deletados
        """
        try:
            id = int(id)
            if not id or id <= 0:
                raise ValueError("ID deve ser um número válido")
            
            if not self.repository.obter_registro(id):
                raise ValueError(f"Produto com ID {id} não encontrado")
            
            return self.repository.excluir_registro(id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao excluir produto: {str(e)}")
    
    def processar_produto(self, acao, descricao=None, preco_unitario=None, quantidade_estoque=None, categoria_id=None, id=None):
        """
        Roteia a operação de produto baseado na ação
        Responsabilidade da service: decidir qual método executar
        
        Args:
            acao: Tipo de ação ('Inclusão', 'Alteração', 'Exclusão')
            descricao: Descrição do produto (obrigatória para Inclusão/Alteração)
            preco_unitario: Preço (obrigatória para Inclusão/Alteração)
            quantidade_estoque: Estoque (obrigatária para Inclusão/Alteração)
            categoria_id: ID da categoria (obrigatória para Inclusão/Alteração)
            id: ID do produto (obrigatória para Alteração/Exclusão)
            
        Returns:
            Resultado da operação
        """
        if acao == 'Exclusão':
            return self.excluir_produto(id)
        elif acao == 'Alteração':
            return self.alterar_produto(id, descricao, preco_unitario, quantidade_estoque, categoria_id)
        else:  
            return self.salvar_produto(descricao, preco_unitario, quantidade_estoque, categoria_id)