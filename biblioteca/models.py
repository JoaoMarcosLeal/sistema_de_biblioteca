from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# --- NOVO ---
class Categoria(models.Model):
    nome = models.CharField("Categoria", max_length=80, unique=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Livro(models.Model):
    nome = models.CharField("Título", max_length=255)
    autor = models.CharField("Autor", max_length=255)
    ano = models.IntegerField("Ano de publicação")
    editora = models.CharField("Editora", max_length=255, null=True, blank=True)
    edicao = models.IntegerField("Edição")
    categorias = models.ManyToManyField(Categoria, blank=True, related_name="livros", verbose_name="Categorias")
    quantidade_total = models.PositiveIntegerField("Qtde total", default=1)
    quantidade_disponivel = models.PositiveIntegerField("Qtde disponível", default=1)

    def __str__(self):
        return f"{self.nome} - {self.autor} - {self.ano} - {self.edicao}a edição"

    def clean(self):
        if self.quantidade_disponivel > self.quantidade_total:
            raise ValidationError("Quantidade disponível não pode exceder a quantidade total.")


class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")

    data_emprestimo = models.DateField("Data do Empréstimo", auto_now_add=True)
    data_devolucao_prevista = models.DateField("Previsão de Devolução")
    devolvido = models.BooleanField("Devolvido", default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.nome} - {self.devolvido}"

    def clean(self):
        if self.pk is None and not self.devolvido:
            if self.livro.quantidade_disponivel < 1:
                raise ValidationError("Sem exemplares disponíveis para este livro.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            criando = self.pk is None
            antigo_devolvido = None
            antigo_livro_id = None
            if not criando:
                antigo = Emprestimo.objects.select_for_update().get(pk=self.pk)
                antigo_devolvido = antigo.devolvido
                antigo_livro_id = antigo.livro_id

            super().save(*args, **kwargs)

            if criando and not self.devolvido:
                if self.livro.quantidade_disponivel > 0:
                    self.livro.quantidade_disponivel -= 1
                    self.livro.save(update_fields=["quantidade_disponivel"])

            elif not criando and antigo_devolvido is False and self.devolvido is True:
                self.livro.quantidade_disponivel = min(
                    self.livro.quantidade_total,
                    self.livro.quantidade_disponivel + 1
                )
                self.livro.save(update_fields=["quantidade_disponivel"])