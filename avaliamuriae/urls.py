from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bem-vindo à página inicial do Avalia Muriae!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend_avalia.urls')),  # Prefixo de API para as rotas do backend
    path('', home),  # Página inicial
]
