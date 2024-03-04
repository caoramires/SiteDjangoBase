
from django.urls import path, reverse_lazy
from .views import Homepage, Dashboard, Dimensoes, Processos, Procedimentos, Editarprocedimento, Editarperfil
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
    path('editarprocedimento/', Editarprocedimento.as_view(), name='editarprocedimento'),
    path('editarperfil/<int:pk>', Editarperfil.as_view(), name='editarperfil'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name="editarperfil.html",
                                                             success_url=reverse_lazy('grc:dashboard')), name='mudarsenha'),

]
