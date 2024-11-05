from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Modelo Escola
class Escola(models.Model):
    nome_escola = models.CharField(max_length=255)
    censo = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_escola


# Modelo Turma
class Turma(models.Model):
    nome_turma = models.CharField(max_length=255)
    ano = models.IntegerField()
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='turmas')

    def __str__(self):
        return f"{self.nome_turma} - {self.ano}"


class Professor(models.Model):
    nome_professor = models.CharField(max_length=255)
    email_professor = models.EmailField(unique=True)
    cpf_professor = models.CharField(max_length=11, unique=True)
    senha_professor = models.CharField(max_length=255)  # Armazenaremos a senha como hash

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)


# Modelo Aluno
class Aluno(models.Model):
    nome_aluno = models.CharField(max_length=255)
    sobrenome_aluno = models.CharField(max_length=255)
    inep_aluno = models.CharField(max_length=12, unique=True)
    data_nascimento = models.DateField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')

    def __str__(self):
        return f"{self.nome_aluno} {self.sobrenome_aluno}"


# Modelo Avaliacao
class Avaliacao(models.Model):
    nome_prova = models.CharField(max_length=255)
    disciplina = models.CharField(max_length=255)
    semestre = models.IntegerField()
    ano = models.IntegerField()
    numero_questoes = models.IntegerField()

    def __str__(self):
        return f"{self.nome_prova} - {self.disciplina} ({self.ano})"


# Modelo Questao
class Questao(models.Model):
    texto_questao = models.TextField()
    numero_questao = models.IntegerField()
    resposta_correta = models.CharField(max_length=255)
    habilidade_questao = models.CharField(max_length=255, null=True, blank=True)
    observacao_pedagogica = models.TextField(null=True, blank=True)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='questoes')

    def __str__(self):
        return f"Questão {self.id} - {self.texto_questao[:50]}..."


# Modelo RespostaAluno
class RespostaAluno(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='respostas')
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='respostas')
    resposta_marcada = models.CharField(max_length=255)

    def __str__(self):
        return f"Resposta de {self.aluno} para Questão {self.questao.id}"


# Modelo ProfessorTurma (relação muitos-para-muitos entre Professor e Turma)
class ProfessorTurma(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='turmas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='professores')

    class Meta:
        unique_together = ('professor', 'turma')

    def __str__(self):
        return f"{self.professor} - {self.turma}"


# Modelo AlunoAvaliacao (relação muitos-para-muitos entre Aluno e Avaliacao)
class AlunoAvaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='alunos')

    class Meta:
        unique_together = ('aluno', 'avaliacao')

    def __str__(self):
        return f"Avaliação {self.avaliacao} do aluno {self.aluno}"

class Admin(models.Model):
    nome_admin = models.CharField(max_length=255)
    sobrenome_admin = models.CharField(max_length=255)
    email_admin = models.EmailField(unique=True)
    senha_admin = models.CharField(max_length=255)  # Armazenaremos a senha como hash
    setor = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.senha_admin = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha_admin)