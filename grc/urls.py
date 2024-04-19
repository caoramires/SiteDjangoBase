
from django.urls import path, reverse_lazy
from .views import Homepage, Dashboard, Dimensoes, Processos, Procedimentos, Editarproc, Editarperfil, Planos, \
    Tarefas, PlanosConcluidos, PlanosCancelados, PlanosPlanejados, EditarTarefa, CriarTarefa, CriarPlano, EditarPlano, \
    ExcluirTarefa, ExcluirPlano, VerificaTarefasPlano, ProcessosPorDimensao, ProcedimentosPorProcesso, \
    EditarProcedimento, Dash, Painel
from django.contrib.auth import views as auth_view

app_name = 'grc'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('grc/', Dashboard.as_view(), name='dashboard'),
    path('painel/', Painel.as_view(), name='painel'),
    path('dash/', Dash.as_view(), name='dash'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dimensoes/', Dimensoes.as_view(), name='dimensoes'),
    path('processos/', Processos.as_view(), name='processos'),
    path('processospordimensao/<int:pk>', ProcessosPorDimensao.as_view(), name='processospordimensao'),
    path('procedimentos/', Procedimentos.as_view(), name='procedimentos'),
    path('procedimentosporprocesso/<int:dm>/<int:pk>', ProcedimentosPorProcesso.as_view(), name='procedimentosporprocesso'),
    path('editarprocedimento/<int:dm>/<int:pk>', EditarProcedimento.as_view(), name='editarprocedimento'),
    path('planos/', Planos.as_view(), name='planos'),
    path('criarplano/', CriarPlano.as_view(), name='criarplano'),
    path('editarplano/<int:pk>', EditarPlano.as_view(), name='editarplano'),
    path('verificatarefasplano/<int:pk>', VerificaTarefasPlano.as_view(), name='verificatarefasplano'),
    path('excluirplano/<int:pk>', ExcluirPlano.as_view(), name='excluirplano'),
    path('planosconcluidos/', PlanosConcluidos.as_view(), name='planosconcluidos'),
    path('planoscancelados/', PlanosCancelados.as_view(), name='planoscancelados'),
    path('planosplanejados/', PlanosPlanejados.as_view(), name='planosplanejados'),
    path('tarefas/<int:id>', Tarefas.as_view(), name='tarefas'),
    path('editartarefa/<int:pk>', EditarTarefa.as_view(), name='editartarefa'),
    path('criartarefa/', CriarTarefa.as_view(), name='criartarefa'),
    path('excluirtarefa/<int:pk>', ExcluirTarefa.as_view(), name='excluirtarefa'),
    path('editarproc/', Editarproc.as_view(), name='editarproc'),
    path('editarproc2/', Editarproc.as_view(), name='editarproc2'),
    path('editarperfil/<int:pk>', Editarperfil.as_view(), name='editarperfil'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name="editarperfil.html",
                                                             success_url=reverse_lazy('grc:dashboard')), name='mudarsenha'),

]
