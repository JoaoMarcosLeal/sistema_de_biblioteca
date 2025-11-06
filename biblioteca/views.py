from django.shortcuts import render
from .models import Livro 

def livros(request):
    livros = Livro.objects.all() 
    context = {
        'livros': livros
    }
    return render(request, 'livros.html', context)

