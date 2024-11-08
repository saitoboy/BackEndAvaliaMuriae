import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Escola, Professor, Turma, Aluno, Avaliacao, Questao, RespostaAluno, Admin
from .serializers import EscolaSerializer, ProfessorSerializer, TurmaSerializer, AlunoSerializer, AvaliacaoSerializer, QuestaoSerializer, RespostaAlunoSerializer, AdminSerializer
from .serializers import UserLoginSerializer,  AdminSignupSerializer, ProfessorSignupSerializer

# View para uma resposta simples na URL base do app
def index(request):
    return HttpResponse("Bem-vindo à seção backend do Avalia Muriae!")

# Viewsets para a API REST
class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    def perform_create(self, serializer):
        professor = serializer.save()
        professor.set_password(professor.senha)
        professor.save()

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    lookup_field = 'id'

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all()
    serializer_class = QuestaoSerializer

class RespostaAlunoViewSet(viewsets.ModelViewSet):
    queryset = RespostaAluno.objects.all()
    serializer_class = RespostaAlunoSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def perform_create(self, serializer):
        admin = serializer.save()
        admin.set_password(admin.senha_admin)
        admin.save()

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            is_admin = serializer.validated_data.get('is_admin')

            # Gera o token JWT
            refresh = RefreshToken.for_user(user)

            # Gera o ID especial usando uuid apenas se for um administrador
            special_id = str(uuid.uuid4()) if is_admin else None

            response_data = {
                'name': user.nome_admin if is_admin else user.nome_professor,
                'token': str(refresh.access_token),
                'special_id': special_id  # Retorna o ID especial apenas para admins
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View de Cadastro para Professor
class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = str(RefreshToken.for_user(user).access_token)
            response_data = {
                'name': user.nome_admin,
                'token': token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View de Cadastro para Professor
class ProfessorSignupView(APIView):
    def post(self, request):
        serializer = ProfessorSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = str(RefreshToken.for_user(user).access_token)
            response_data = {
                'name': user.nome_professor,
                'token': token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
