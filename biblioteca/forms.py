# biblioteca/forms.py
from django import forms
from .models import Livro, Categoria
import csv
from io import StringIO


class LivroImportForm(forms.Form):
    file = forms.FileField(label="Escolha um arquivo CSV")

    def process_csv(self):
        # Lê o arquivo CSV enviado
        csv_file = self.cleaned_data["file"]
        decoded_file = csv_file.read().decode("utf-8")  # Decode para UTF-8

        # Cria um buffer de memória
        io_string = StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=",", quotechar='"')

        # Ignora o cabeçalho do CSV
        next(reader)

        # Itera sobre cada linha no arquivo CSV
        livros_adicionados = 0
        for row in reader:
            nome, autor, ano, editora, edicao, categorias, quantidade_total, quantidade_disponivel = row
            livro = Livro.objects.create(
                nome=nome,
                autor=autor,
                ano=ano,
                editora=editora,
                edicao=edicao,
                quantidade_total=quantidade_total,
                quantidade_disponivel=quantidade_disponivel
            )
            
            # Adiciona categorias, se houver
            for categoria_nome in categorias.split(','):
                categoria_obj = Categoria.objects.get(nome=categoria_nome.strip())
                livro.categorias.add(categoria_obj)

            livros_adicionados += 1

        return livros_adicionados
