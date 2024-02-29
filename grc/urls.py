
from django.urls import path
from .views import Homepage, Dashboard, Dimensoes
from django.contrib.auth import views as auth_view

app_name = 'grc'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('grc/', Dashboard.as_view(), name='dashboard'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dimensoes/', Dimensoes.as_view(), name='dimensoes'),

]
