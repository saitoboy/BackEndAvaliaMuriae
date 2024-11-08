from rest_framework import serializers
from .models import Escola, Professor, Turma, Aluno, Avaliacao, Questao, RespostaAluno, Admin
from rest_framework_simplejwt.tokens import RefreshToken

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questao
        fields = '__all__'

class RespostaAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespostaAluno
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        senha = data.get("senha")

        # Verifica se o usuário é um administrador
        try:
            admin = Admin.objects.get(email_admin=email)
            if admin.check_password(senha):
                data['user'] = admin
                data['is_admin'] = True
                return data
        except Admin.DoesNotExist:
            pass

        # Verifica se o usuário é um professor
        try:
            professor = Professor.objects.get(email_professor=email)
            if professor.check_password(senha):
                data['user'] = professor
                data['is_admin'] = False
                return data
        except Professor.DoesNotExist:
            pass

        # Se o usuário não for encontrado ou a senha estiver incorreta
        raise serializers.ValidationError("Credenciais de login inválidas")

# Serializer de Cadastro para Admin
class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['nome_admin', 'sobrenome_admin', 'email_admin', 'senha_admin', 'setor']
        extra_kwargs = {'senha_admin': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('senha_admin')
        admin = Admin(**validated_data)
        admin.set_password(senha)
        admin.save()
        return admin

# Serializer de Cadastro para Professor
class ProfessorSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['nome_professor', 'sobrenome_professor','cpf_professor', 'email_professor', 'senha_professor']
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('senha_professor')
        professor = Professor(**validated_data)
        professor.set_password(senha)
        professor.save()
        return professor
