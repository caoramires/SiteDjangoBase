from django.shortcuts import redirect, reverse
from .models import Framework
from .forms import FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# Create your views here.

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        # se usuário está autenticado
        if request.user.is_authenticated:
            # envia para dashboard
            return redirect('grc:dashboard')
        else:
            # do contrário mantém na home fechada
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = User.objects.filter(email=email)
        if usuarios:
            return reverse('grc:login')
        else:
            return reverse('grc:homepage')

class Dashboard(ListView):
    template_name = "dashboard.html"
    model = Framework

