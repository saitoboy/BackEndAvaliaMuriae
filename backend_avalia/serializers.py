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

class AdminLoginSerializer(serializers.Serializer):
    email_admin = serializers.EmailField()
    senha_admin = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email_admin")
        senha = data.get("senha_admin")

        try:
            admin = Admin.objects.get(email_admin=email)
            if not admin.check_password(senha):
                raise serializers.ValidationError("Credenciais de login inválidas")
        except Admin.DoesNotExist:
            raise serializers.ValidationError("Credenciais de login inválidas")

        refresh = RefreshToken.for_user(admin)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ProfessorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        senha = data.get("senha")

        try:
            professor = Professor.objects.get(email=email)
            if not professor.check_password(senha):
                raise serializers.ValidationError("Credenciais de login inválidas")
        except Professor.DoesNotExist:
            raise serializers.ValidationError("Credenciais de login inválidas")

        refresh = RefreshToken.for_user(professor)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
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
        fields = ['nome_professor', 'email', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        professor = Professor(**validated_data)
        professor.set_password(senha)
        professor.save()
        return professor