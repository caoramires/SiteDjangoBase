from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView

# Create your views here.

class Homepage(TemplateView):
    template_name = 'homepage.html'
