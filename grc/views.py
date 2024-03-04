from django.shortcuts import redirect, reverse
from .models import Framework, Dimension, Processo, Procedimento
from .forms import FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# Create your views here.

class Homepage(TemplateView):
    template_name = 'homepage.html'


class Dashboard(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    model = Dimension

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dimensoes"] = Dimension.objects.all()
        return context

class Dimensoes(LoginRequiredMixin, ListView):
    template_name = "dimensoes.html"
    model = Dimension
    model = Processo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dimensoes"] = Dimension.objects.all()
        return context

class Processos(LoginRequiredMixin, ListView):
    template_name = "processos.html"
    model = Processo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["processos"] = Processo.objects.all()
        return context

class Procedimentos(LoginRequiredMixin, ListView):
    template_name = "procedimentos.html"
    model = Procedimento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["procedimentos"] = Procedimento.objects.all()
        context["processos"] = Processo.objects.all().prefetch_related('procedimento')
        return context

class Editarprocedimento(LoginRequiredMixin, UpdateView):
    template_name = 'editarprocedimento.html'
    model = Procedimento
    fields = ['atendido']

    def get_success_url(self):
        return reverse('grc:procedimentos')

class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = User
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('grc:dashboard')