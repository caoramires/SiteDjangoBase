
from django.urls import path, reverse_lazy
from .views import Homepage, Dashboard, Dimensoes, Processos, Procedimentos, Editarproc, Editarperfil, Planos, \
    Tarefas, PlanosConcluidos, PlanosCancelados, PlanosPlanejados, EditarTarefa, CriarTarefa
from django.contrib.auth import views as auth_view

app_name = 'grc'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('grc/', Dashboard.as_view(), name='dashboard'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dimensoes/', Dimensoes.as_view(), name='dimensoes'),
    path('processos/', Processos.as_view(), name='processos'),
    path('procedimentos/', Procedimentos.as_view(), name='procedimentos'),
    path('planos/', Planos.as_view(), name='planos'),
    path('planosconcluidos/', PlanosConcluidos.as_view(), name='planosconcluidos'),
    path('planoscancelados/', PlanosCancelados.as_view(), name='planoscancelados'),
    path('planosplanejados/', PlanosPlanejados.as_view(), name='planosplanejados'),
    path('tarefas/<int:plano_id>', Tarefas.as_view(), name='tarefas'),
    path('editartarefa/<int:tarefa_id>', EditarTarefa.as_view(), name='editartarefa'),
    path('criartarefa/', CriarTarefa.as_view(), name='criartarefa'),
    path('editarproc/', Editarproc.as_view(), name='editarproc'),
    path('editarproc2/', Editarproc.as_view(), name='editarproc2'),
    path('editarplano/', Editarproc.as_view(), name='editarplano'),
    path('editarperfil/<int:pk>', Editarperfil.as_view(), name='editarperfil'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name="editarperfil.html",
                                                             success_url=reverse_lazy('grc:dashboard')), name='mudarsenha'),

]
