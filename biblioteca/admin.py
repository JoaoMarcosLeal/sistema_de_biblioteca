from datetime import timedelta
from django.contrib import admin
from django.utils import timezone
from django.db import transaction
from .models import Livro, Emprestimo, Categoria

@admin.action(description="Marcar empréstimos selecionados como DEVOLVIDOS (ajusta estoque)")
def marcar_como_devolvido(modeladmin, request, queryset):
    count = 0
    with transaction.atomic():
        for emp in queryset.select_for_update():
            if not emp.devolvido:
                emp.devolvido = True
                emp.save()
                count += 1
    modeladmin.message_user(request, f"{count} empréstimo(s) marcado(s) como devolvido(s).")


@admin.action(description="Marcar empréstimos selecionados como NÃO devolvidos (não ajusta estoque retroativo)")
def marcar_como_nao_devolvido(modeladmin, request, queryset):
    atualizados = queryset.update(devolvido=False)
    modeladmin.message_user(request, f"{atualizados} empréstimo(s) marcado(s) como NÃO devolvido(s).")


@admin.action(description="Prorrogar previsão em +7 dias")
def prorrogar_sete_dias(modeladmin, request, queryset):
    count = 0
    for emp in queryset:
        emp.data_devolucao_prevista = emp.data_devolucao_prevista + timedelta(days=7)
        emp.save(update_fields=["data_devolucao_prevista"])
        count += 1
    modeladmin.message_user(request, f"Previsão prorrogada em 7 dias para {count} empréstimo(s).")



@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("nome", "autor", "ano", "edicao", "editora", "quantidade_total", "quantidade_disponivel")
    list_filter = ("editora", "ano", "categorias")
    search_fields = ("nome", "autor", "editora")
    filter_horizontal = ("categorias",)
    ordering = ("nome",)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "livro",
        "data_emprestimo",
        "data_devolucao_prevista",
        "devolvido",
        "em_atraso",
    )
    list_filter = (
        "devolvido",
        "data_emprestimo",
        "data_devolucao_prevista",
        "livro__editora",
        "livro__categorias",
    )
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "livro__nome",
        "livro__autor",
        "livro__editora",
    )
    date_hierarchy = "data_emprestimo"
    ordering = ("-data_emprestimo",)
    actions = [marcar_como_devolvido, marcar_como_nao_devolvido, prorrogar_sete_dias]
    autocomplete_fields = ("usuario", "livro")

    @admin.display(boolean=True, description="Em atraso?")
    def em_atraso(self, obj):
        if obj.devolvido:
            return False
        hoje = timezone.localdate()
        return hoje > obj.data_devolucao_prevista
