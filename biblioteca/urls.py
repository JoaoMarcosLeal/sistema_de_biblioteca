from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_livros, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('importar_livros/', views.importar_livros, name='importar_livros'),
    path('emprestimo/', views.emprestimo_multiplo, name='emprestimo_multiplo'),
]
