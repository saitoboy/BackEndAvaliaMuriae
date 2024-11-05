from django.contrib import admin
from .models import Escola, Professor, Turma, Aluno, Avaliacao, Questao, RespostaAluno

admin.site.register(Escola)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Avaliacao)
admin.site.register(Questao)
admin.site.register(RespostaAluno)