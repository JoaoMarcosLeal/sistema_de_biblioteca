from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro, Categoria, Emprestimo
from .forms import LivroImportForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

def login_view(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next', 'home')
        return redirect(next_url) 
    next_url = request.GET.get('next', '')  
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(next_url or 'home') 
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, "login.html", {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def lista_livros(request):
    categoria_id = request.GET.get("categoria_id")
    categorias = Categoria.objects.all()
    livros = Livro.objects.all()
    titulo_pagina = "Lista de Todos os Livros"
    categoria_selecionada = None

    if categoria_id and categoria_id != "0":
        try:
            categoria_id_int = int(categoria_id)
            categoria_selecionada = get_object_or_404(Categoria, pk=categoria_id_int)
            livros = livros.filter(categorias=categoria_selecionada)
            titulo_pagina = f"Livros na Categoria: {categoria_selecionada.nome}"
        except ValueError:
            messages.error(request, "Categoria inválida.")
            return redirect('home')

    context = {
        "livros": livros,
        "categorias": categorias,
        "titulo_pagina": titulo_pagina,
        "categoria_selecionada_id": categoria_id,
    }
    return render(request, "livros.html", context)

def importar_livros(request):
    if request.method == "POST":
        form = LivroImportForm(request.POST, request.FILES)

        if form.is_valid():
            livros_adicionados = form.process_csv()
            messages.success(request, f"{livros_adicionados} livros foram adicionados com sucesso!")
        else:
            messages.error(request, "Houve um erro ao tentar importar os livros.")
    else:
        form = LivroImportForm()

    return render(request, "importar_livros.html", {"form": form})

@login_required
def emprestimo_multiplo(request):
    livros = Livro.objects.all()

    if request.method == "POST":
        livros_ids = request.POST.getlist("livros")
        data_devolucao = request.POST.get("data_devolucao")

        if not data_devolucao:
            messages.error(request, "Por favor, selecione uma data de devolução.")
            return redirect('emprestimo_multiplo')


        for livro_id in livros_ids:
            livro = Livro.objects.get(id=livro_id)

            if livro.quantidade_disponivel <= 0:
                messages.error(request, f"Não há exemplares disponíveis para o livro {livro.nome}.")
                continue

            Emprestimo.objects.create(
                usuario=request.user,
                livro=livro,
                data_devolucao_prevista=data_devolucao
            )

        messages.success(request, "Os livros foram emprestados com sucesso!")
        return redirect('home')

    return render(request, "emprestimo.html", {"livros": livros})