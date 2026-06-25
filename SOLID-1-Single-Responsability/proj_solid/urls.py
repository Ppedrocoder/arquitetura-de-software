"""
URL configuration for proj_bd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # define as rotas de URL da nossa aplicacao
    path('', views.home, name='home'),
    
    # path('instrucoes/', 'instrucoes/instrucoes.html', name='instrucoes'),



    # ===========================================================================
    # Rotas: CATEGORIA
    #   - categorias/              : exibe página de listagem
    #   - categorias/incluir/      : exibe a página de inclusao de registro
    #   - categorias/alterar/<id>/ : exibe a página de alteracao de registro
    #   - categorias/excluir/<id>/ : exibe a página de exclusao de registro
    #   - categorias/salvar/       : insere, altera ou exclui um registro do BD
    # 
    path('categorias/', views.listar_categorias, name='categorias'),
#    path('categorias/<str:acao>/', views.categorias, name='categorias' ), 
    path('categorias/incluir/', views.incluir_categoria, name='categorias_incluir' ), 
    path('categorias/alterar/<int:id>/', views.alterar_categoria, name='categorias_alterar' ), 
    path('categorias/excluir/<int:id>/', views.excluir_categoria, name='categorias_excluir' ), 
    path('categorias/salvar/', views.salvar_categoria, name='categorias_salvar' ),
#    path('categorias/<str:acao>/<int:id>/', views.categorias, name='categorias' ),

    # ===========================================================================
    # Rotas: PRODUTO
    #   - produtos/              : exibe página de listagem
    #   - produtos/incluir/      : exibe a página de inclusao de registro
    #   - produtos/alterar/<id>/ : exibe a página de alteracao de registro
    #   - produtos/excluir/<id>/ : exibe a página de exclusao de registro
    #   - produtos/salvar/       : insere, altera ou exclui um registro do BD
    # 
    path('produtos/', views.listar_produtos, name='produtos'),
#    path('produtos/<str:acao>/', views.produtos, name='produtos' ), 
    path('produtos/incluir/', views.incluir_produto, name='produtos_incluir' ),
    path('produtos/alterar/<int:id>/', views.alterar_produto, name='produtos_alterar' ),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='produtos_excluir' ),
    path('produtos/salvar/', views.salvar_produto, name='produtos_salvar' ),
#    path('produtos/<str:acao>/<int:id>/', views.produtos, name='produtos'),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
