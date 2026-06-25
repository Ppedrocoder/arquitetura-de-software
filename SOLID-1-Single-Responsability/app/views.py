from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from .factory import ServiceFactory

class CategoriaForm(forms.Form):
    """Formulário para edição de categorias"""
    id = forms.IntegerField(
        label='ID', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), 
        required=False
    )
    descricao = forms.CharField(
        label='Descrição', 
        max_length=30, 
        required=True
    )


def salvar_categoria(request):
    """Salva categoria (incluir, alterar ou excluir)
    
    POST /categorias/salvar/
    """
    try:
        acao = request.POST.get('acao')
        id_categoria = request.POST.get('id')
        descricao = request.POST.get('descricao')
        service = ServiceFactory.criar_categoria_service()
        service.processar_categoria(acao, descricao, id_categoria)

        return HttpResponseRedirect(reverse("categorias"))
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

def listar_categorias(request):
    """Lista todas as categorias
    
    GET /categorias/
    """
    try:
        service = ServiceFactory.criar_categoria_service()
        registros = service.listar_registros()
        return render(request, 'categorias_listar.html', context={'registros': registros})
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

def incluir_categoria(request):
    """Exibe formulário para incluir categoria"""
    return render(
        request, 
        'categorias_editar.html',
        context={'acao': 'Inclusão', 'form': CategoriaForm()}
    )

def alterar_categoria(request, id):
    """Exibe formulário para alterar categoria"""
    try:
        service = ServiceFactory.criar_categoria_service()
        registro = service.obter_registro(id)
        
        registro_dict = {
            'id': registro[0], 
            'descricao': registro[1]
        }

        return render(
            request, 
            'categorias_editar.html', 
            context={'acao': 'Alteração', 'form': CategoriaForm(initial=registro_dict)}
        )
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

def excluir_categoria(request, id):
    """Exibe formulário para excluir categoria"""
    try:
        service = ServiceFactory.criar_categoria_service()
        registro = service.obter_registro(id)
        
        registro_dict = {
            'id': registro[0], 
            'descricao': registro[1]
        }

        return render(
            request, 
            'categorias_editar.html', 
            context={'acao': 'Exclusão', 'form': CategoriaForm(initial=registro_dict)}
        )
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)
    preco_unitario = forms.DecimalField(label='Preço Unitário', max_digits=10, decimal_places=2, required=True)
    quantidade_estoque = forms.IntegerField(label='Qtd. Estoque', required=True)
    categoria_id = forms.ChoiceField(label='Categoria', required=True)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            service = ServiceFactory.criar_categoria_service()
            categorias = service.listar_registros()
            self.fields['categoria_id'].choices = categorias


def listar_produtos(request):
    """Lista todos os produtos"""
    try:
        service = ServiceFactory.criar_produto_service()
        registros = service.listar_registros()
        return render(request, 'produtos_listar.html', context={'registros': registros})
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

def salvar_produto(request):
    """Processa salvar/alterar/excluir de produto via formulário"""
    try:
        acao = request.POST.get('acao')
        id_produto = request.POST.get('id')
        descricao = request.POST.get('descricao')
        preco_unitario = request.POST.get('preco_unitario')
        quantidade_estoque = request.POST.get('quantidade_estoque')
        categoria_id = request.POST.get('categoria_id')
        
        service = ServiceFactory.criar_produto_service()
        service.processar_produto(acao, descricao, preco_unitario, quantidade_estoque, categoria_id, id_produto)

        return HttpResponseRedirect(reverse("produtos"))
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

def incluir_produto(request):
    """Exibe formulário para incluir produto"""
    return render(request, 'produtos_editar.html',
                  context={'acao': 'Inclusão', 'form': ProdutoForm()})

def alterar_produto(request, id):
    """Exibe formulário para alterar produto"""
    try:
        service = ServiceFactory.criar_produto_service()
        registro = service.obter_registro(id)
        if not registro:
            raise Exception(f"Produto com ID {id} não encontrado")

        registro_dict = {
            'id': registro[0],
            'descricao': registro[1],
            'preco_unitario': registro[2],
            'quantidade_estoque': registro[3],
            'categoria_id': registro[4]
        }

        return render(request, 'produtos_editar.html', 
                      context={'acao': 'Alteração', 'form': ProdutoForm(initial=registro_dict)})
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

def excluir_produto(request, id):
    """Exibe formulário para excluir produto"""
    try:
        service = ServiceFactory.criar_produto_service()
        registro = service.obter_registro(id)
        if not registro:
            raise Exception(f"Produto com ID {id} não encontrado")

        registro_dict = {
            'id': registro[0],
            'descricao': registro[1],
            'preco_unitario': registro[2],
            'quantidade_estoque': registro[3],
            'categoria_id': registro[4]
        }

        return render(request, 'produtos_editar.html', 
                      context={'acao': 'Exclusão', 'form': ProdutoForm(initial=registro_dict)})
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


def home(request):
    '''Exibe a pagina inicial da aplicação'''
    template = 'home.html'
    return render(request, template)


