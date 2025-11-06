from django.shortcuts import render, get_object_or_404
from .models import Livro, Categoria


# catalogo/views.py

from django.shortcuts import render, get_object_or_404
from .models import Livro, Categoria


def lista_livros(request):
    categoria_id = request.GET.get("categoria_id")  

    categorias = Categoria.objects.all()

    livros = Livro.objects.all()
    titulo_pagina = "Lista de Todos os Livros"
    categoria_selecionada = None  

    if (
        categoria_id and categoria_id != "0"
    ):  
        try:
            categoria_id = int(categoria_id)
            categoria_selecionada = get_object_or_404(Categoria, pk=categoria_id)

            livros = livros.filter(categorias=categoria_selecionada)

            titulo_pagina = f"Livros na Categoria: {categoria_selecionada.nome}"
        except ValueError:
            pass

    context = {
        "livros": livros,
        "categorias": categorias,
        "titulo_pagina": titulo_pagina,
        "categoria_selecionada_id": categoria_id,  
    }

    return render(request, "livros.html", context)
