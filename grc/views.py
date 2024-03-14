from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import EditarAtenderForm, EditarTarefaForm
from .models import Framework, Dimension, Processo, Procedimento, Plano, Tarefa
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
import json



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

class Editarproc2(LoginRequiredMixin, View):
    template_name = 'editarprocpage2.html'
    form_class = EditarAtenderForm

    def get_context_data(self):
        context = {}
        context['procedimentos'] = Procedimento.objects.all()
        context['situacao_atual'] = [procedimento.atendida for procedimento in context['procedimentos']]
        context['LISTA_SITUACAO'] = [('SIM', 'Sim'), ('EmP', 'Em parte'), ('NAO', 'Não')]
        context['form'] = self.form_class
        return context

class Editarproc(LoginRequiredMixin, FormView):
    template_name = 'editarprocpage.html'
    form_class = EditarAtenderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedimentos'] = Procedimento.objects.all()
        context['situacao_atual'] = [procedimento.atendida for procedimento in context['procedimentos']]
        context['LISTA_SITUACAO'] = [('SIM', 'Sim'), ('EmP', 'Em parte'), ('NAO', 'Não')]
        context['form'] = self.form_class
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['procedimentos'] = Procedimento.objects.all()
        return kwargs

    def form_valid(self, form):
        atendida_values = self.request.POST.getlist('atendida_values')
        for atendida in atendida_values:
            pk, value = atendida.split('-')
            procedimento = Procedimento.objects.get(pk=pk)
            procedimento.atendida = value
            procedimento.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('form.cleaned ===',form.cleaned_data.items())
        print('request.POST ====' ,self.request.POST.getlist('atendida_values'))
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = User
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('grc:dashboard')


class Planos(LoginRequiredMixin, ListView):
    template_name = "planos.html"
    model = Plano

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planos_andamento = Plano.objects.filter(status="ANDAMENTO")
        context["planos_andamento"] = planos_andamento
        return context

class PlanosConcluidos(LoginRequiredMixin, ListView):
    template_name = "planosconcluidos.html"
    model = Plano

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planos_concluidos = Plano.objects.filter(status="CONCLUIDO")
        context["planos_concluidos"] = planos_concluidos
        return context

class PlanosCancelados(LoginRequiredMixin, ListView):
    template_name = "planoscancelados.html"
    model = Plano

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planos_cancelados = Plano.objects.filter(status="CANCELADO")
        context["planos_cancelados"] = planos_cancelados
        return context

class PlanosPlanejados(LoginRequiredMixin, ListView):
    template_name = "planosplanejados.html"
    model = Plano

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planos_planejados = Plano.objects.filter(status = "PLANEJADO")
        context["planos_planejados"] = planos_planejados
        return context

class EditarPlano(LoginRequiredMixin, ListView):
    template_name = "editarplano.html"
    model = Plano

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["planos"] = Plano.objects.all()
        return context


class Tarefas(LoginRequiredMixin, ListView):
    template_name = "tarefas.html"
    model = Tarefa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano = self.kwargs.get('plano_id')
        tarefas_plano = Tarefa.objects.filter(plano=plano)
        context["tarefas_plano"] = tarefas_plano
        return context

class EditarTarefa(LoginRequiredMixin, FormView):
    template_name = "editartarefa.html"
    model = Tarefa
    form_class = EditarTarefaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('tarefa_id')
        tarefa = Tarefa.objects.filter(pk=pk)
        context["tarefa"] = tarefa
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('grc:planos')


class CriarTarefa(LoginRequiredMixin, FormView):
    template_name = "criartarefa.html"
    model = Tarefa
    form_class = EditarTarefaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('tarefa_id')
        tarefa = Tarefa.objects.filter(pk=pk)
        context["tarefa"] = tarefa
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('grc:planos')