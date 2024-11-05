from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('escolas/', views.EscolaViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('professores/', views.ProfessorViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('turmas/', views.TurmaViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('alunos/', views.AlunoViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('avaliacoes/', views.AvaliacaoViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('questoes/', views.QuestaoViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('respostas_alunos/', views.RespostaAlunoViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('admin/', views.AdminViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),


    # Rotas de Login e Cadastro para Admin
    path('admin/login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('admin/signup/', views.AdminSignupView.as_view(), name='admin-signup'),

    # Rotas de Login e Cadastro para Professor
    path('professor/login/', views.ProfessorLoginView.as_view(), name='professor-login'),
    path('professor/signup/', views.ProfessorSignupView.as_view(), name='professor-signup'),
]
