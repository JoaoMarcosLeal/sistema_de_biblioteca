from django.db import models
from django.contrib.auth.models import User


class Livro(models.Model):
    nome = models.CharField("Título", max_length=255)
    autor = models.CharField("Autor", max_length=255)
    ano = models.IntegerField("Ano de publicação")
    editora = models.CharField("Editora", max_length=255, null=True)
    edicao = models.IntegerField("Edição")

    def __str__(self):
        return f"{self.nome} - {self.autor} - {self.ano} - {self.edicao}a edição"


class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")

    data_emprestimo = models.DateField("Data do Empréstimo", auto_now_add=True)
    data_devolucao_prevista = models.DateField("Previsão de Devolução")
    devolvido = models.BooleanField("Devolvido", default=False)
