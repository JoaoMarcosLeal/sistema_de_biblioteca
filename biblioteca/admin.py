from django.contrib import admin
from .models import Livro
from .models import Emprestimo

admin.site.register(Livro)
admin.site.register(Emprestimo)