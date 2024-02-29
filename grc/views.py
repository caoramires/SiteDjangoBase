from django.shortcuts import redirect, reverse
from .models import Framework, Dimension, Processo
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
