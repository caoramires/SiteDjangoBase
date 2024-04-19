from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import EditarAtenderForm, EditarTarefaForm, CriarPlanoForm, EditarProcedimentoForm
from .models import Framework, Dimension, Processo, Procedimento, Plano, Tarefa
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, UpdateView, View, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.utils import timezone
import datetime
from django.db.models import Count
import plotly.graph_objects as go
import plotly.offline as opy
import pandas as pd
import plotly.express as px

class Homepage(TemplateView):
    template_name = 'homepage.html'


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    model = Dimension
    model = Procedimento

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        # Consolida atendida por Processo
        dimensao_data = {}
        for dimensao in Dimension.objects.all():
            processo_data = {}
            for processo in dimensao.processo.all():
                if processo.procedimento.all():
                    procedimentos = processo.procedimento.all()
                    processo_data[processo] = {
                        'sim': procedimentos.filter(atendida='SIM').count(),
                        'nao': procedimentos.filter(atendida='NAO').count(),
                        'emp': procedimentos.filter(atendida='EmP').count(),
                    }
                    total_processo = sum(processo_data[processo].values())
                    processo_data[processo]['total'] = total_processo
                else:
                    processo_data[processo] = {
                        'sim': 0,
                        'nao': 0,
                        'emp': 0,
                    }
                    total_processo = 0
                    processo_data[processo]['total'] = total_processo
            dimensao_data[dimensao] = processo_data

        print('-----------------------------------------------------------')
        print(f' Dimensao_data >>>>> {dimensao_data}')
        print('-----------------------------------------------------------')


        # cria dict auxiliar para plotagem
        df_data = {}
        for dimensao, processo_data in dimensao_data.items():

            for processo, contagem in processo_data.items():
                if 'total' not in contagem:
                    contagem['total'] = 0  # Preencher com 0 se a chave não existir

                df_data.setdefault(dimensao, []).append({
                    'dimensao': dimensao.nome,
                    'processo': processo.nome,
                    'sim': contagem['sim'],
                    'nao': contagem['nao'],
                    'emp': contagem['emp'],
                    'total': contagem['total'],
                })

        for dimensao, processos in df_data.items():
            for processo in processos:
                # Verificar se a chave 'total' existe
                if 'total' not in processo:
                    processo['total'] = 0

        print('-----------------------------------------------------------')
        print(f' DF_DATA >>>>> {df_data}')
        print('-----------------------------------------------------------')

        # cria df para a plotagem

        # Inicializar variáveis para totais

        totais_por_dimensao = {}
        lista_totais_dimensao =[]

        # Iterar sobre o dicionário df_data
        for dimensao, processos in df_data.items():
            # Inicializar variáveis acumuladoras
            total_sim = 0
            total_nao = 0
            total_emp = 0
            numero_processos = 0
            dimensao_nome = dimensao.nome

            # Processar cada processo

            for processo in processos:
                total_sim += processo['sim']
                total_nao += processo['nao']
                total_emp += processo['emp']
                numero_processos += 1

            numero_procedimentos = total_sim + total_nao + total_emp

            # Armazenar totais no dicionário auxiliar
            # totais_por_dimensao[dimensao] = {
            #     'Dimensao' : dimensao.nome,
            #     'SIM': total_sim,
            #     'NAO': total_nao,
            #     'EMP': total_emp,
            #     'Processos': numero_processos,
            #     'Procedimentos': numero_procedimentos,
            # }

            lista_totais_dimensao.append({
                'Dimensao': dimensao.nome,
                'SIM': total_sim,
                'NAO': total_nao,
                'EMP': total_emp,
                'Processos': numero_processos,
                'Procedimentos': numero_procedimentos,
            }
            )
        print('-----------------------------------------------------------')
        # print(f'TOTAIS DIMENSAO {totais_por_dimensao}')
        print('-----------------------------------------------------------')
        print('-----------------------------------------------------------')
        print(f'LISTA TOTAIS DIMENSAO {lista_totais_dimensao}')
        print('-----------------------------------------------------------')

        labels = []
        datasets = []

        for item in lista_totais_dimensao:
            labels.append(item['Dimensao'])
            datasets.append({
                'label': 'SIM',
                'data': item['SIM'],
                'backgroundColor': '#696969',
            }),
            datasets.append( {
                'label': 'NÃO',
                'data': item['NAO'],
                'backgroundColor': '#808080',
            }),
            datasets.append({
                'label': 'EMP',
                'data': item['EMP'],
                'backgroundColor': '#C0C0C0',
            })

        print(f'LABEL   {labels}   DATASETS   {datasets}')

        context['dimensao_data'] = dimensao_data
        context['labels'] = json.dumps(labels)
        context['datasets'] = json.dumps(datasets)
        return context


class Painel(TemplateView):
    template_name = "painel.html"
    model = Dimension
    model = Procedimento
    model = Plano

    def get(self, request, **kwargs):
        context = super(Painel, self).get_context_data(**kwargs)

        # Consolida atendida por Processo
        dimensao_data = {}
        for dimensao in Dimension.objects.all():
            processo_data = {}
            for processo in dimensao.processo.all():
                if processo.procedimento.all():
                    procedimentos = processo.procedimento.all()
                    processo_data[processo] = {
                        'sim': procedimentos.filter(atendida='SIM').count(),
                        'nao': procedimentos.filter(atendida='NAO').count(),
                        'emp': procedimentos.filter(atendida='EmP').count(),
                    }
                    total_processo = sum(processo_data[processo].values())
                    processo_data[processo]['total'] = total_processo
                else:
                    processo_data[processo] = {
                        'sim': 0,
                        'nao': 0,
                        'emp': 0,
                    }
                    total_processo = 0
                    processo_data[processo]['total'] = total_processo
            dimensao_data[dimensao] = processo_data

        print('-----------------------------------------------------------')
        print(f' Dimensao_DATA >>>>> {dimensao_data}')
        print('-----------------------------------------------------------')


        # cria dict auxiliar para plotagem
        df_data = {}
        for dimensao, processo_data in dimensao_data.items():

            for processo, contagem in processo_data.items():
                if 'total' not in contagem:
                    contagem['total'] = 0  # Preencher com 0 se a chave não existir

                df_data.setdefault(dimensao, []).append({
                    'dimensao': dimensao.nome,
                    'processo': processo.nome,
                    'sim': contagem['sim'],
                    'nao': contagem['nao'],
                    'emp': contagem['emp'],
                    'total': contagem['total'],
                })

        print('-----------------------------------------------------------')
        print(f' DF_DATA >>>>> {df_data}')
        print('-----------------------------------------------------------')


        for dimensao, processos in df_data.items():
            for processo in processos:
                # Verificar se a chave 'total' existe
                if 'total' not in processo:
                    processo['total'] = 0

        # cria df para a plotagem

        lista_totais_dimensao = []

        # Iterar sobre o dicionário df_data
        for dimensao, processos in df_data.items():
            total_sim = 0
            total_nao = 0
            total_emp = 0
            numero_processos = 0
            dimensao_nome = dimensao.nome

            # Processar cada processo

            for processo in processos:
                total_sim += processo['sim']
                total_nao += processo['nao']
                total_emp += processo['emp']
                numero_processos += 1

            numero_procedimentos = total_sim + total_nao + total_emp


            lista_totais_dimensao.append({
                'Dimensao': dimensao.nome,
                'SIM': total_sim,
                'NAO': total_nao,
                'EMP': total_emp,
                'Processos': numero_processos,
                'Procedimentos': numero_procedimentos,
            }
            )


        labels = []
        sim = []
        nao = []
        emp = []

        for item in lista_totais_dimensao:
            labels.append(item['Dimensao'])
            sim.append(item['SIM'])
            nao.append(item['NAO'])
            emp.append(item['EMP'])

        datasets = [{"label":"Sim", "data": sim}, {"label":"Nao", "data": nao},{"label":"Em Parte", "data": emp}]

        labels_json = json.dumps(labels)
        datasets_json = json.dumps(datasets)

        print('-----------------------------------------------------------')
        print(f' labels_json  {labels_json}')
        print('-----------------------------------------------------------')
        print('-----------------------------------------------------------')
        print(f' datasets_json {datasets_json}')
        print('-----------------------------------------------------------')

    # Prepara dados de Planos para Plotagem

        # Conta as ações por processo/Procedimento



        print('-----------------------------------------------------------')
        print(f' dimensao_processos_dic ')
        print('-----------------------------------------------------------')

        hoje = timezone.now()
        planos_atrasados = []









        # Associa Número de Ações de Processo à Dimensão

        # print(f'planos_processo  {planos}')


        context['dimensao_data'] = dimensao_data
        context['labels'] = labels_json
        context['datasets'] = datasets_json

        return render(request, 'painel.html', context)




class Dash(TemplateView):
    template_name = "dash.html"
    model = Dimension
    model = Procedimento

    def get(self, request):
        emp_data = [
            {"label": "IDENTIFICAR", "y": 60},
            {"label": "PROTEGER", "y": 30},
            {"label": "DETECTAR", "y": 25},
            {"label": "RESPONDER", "y": 30},
            {"label": "RECUPERAR", "y": 35},

        ]

        sim_data = [
            {"label": "IDENTIFICAR", "y": 45},
            {"label": "PROTEGER", "y": 20},
            {"label": "DETECTAR", "y": 25},
            {"label": "RESPONDER", "y": 20},
            {"label": "RECUPERAR", "y": 25},

        ]

        nao_data = [
            {"label": "IDENTIFICAR", "y": 0},
            {"label": "PROTEGER", "y": 25},
            {"label": "DETECTAR", "y": 20},
            {"label": "RESPONDER", "y": 25},
            {"label": "RECUPERAR", "y": 45},

        ]

        july_data = [
            {"y": 450, "label": "RECUPERAR"},
            {"y": 70, "label": "RESPONDER"},
            {"y": 200, "label": "DETECTAR"},
            {"y": 324, "label": "PROTEGER"},
            {"y": 300, "label": "IDENTIFICAR"}
        ]
        august_data = [
            {"y": 550, "label": "RECUPERAR"},
            {"y": 270, "label": "RESPONDER"},
            {"y": 400, "label": "DETECTAR"},
            {"y": 524, "label": "PROTEGER"},
            {"y": 500, "label": "IDENTIFICAR"}
        ]
        september_data = [
            {"y": 660, "label": "RECUPERAR"},
            {"y": 265, "label": "RESPONDER"},
            {"y": 271, "label": "DETECTAR"},
            {"y": 360, "label": "PROTEGER"},
            {"y": 340, "label": "IDENTIFICAR"}
        ]

        return render(request, 'dash.html',
                      {"emp_data": emp_data, "sim_data": sim_data, "nao_data": nao_data, "july_data" : july_data, "august_data": august_data, "september_data": september_data})


class Dimensoes(LoginRequiredMixin, ListView):
    template_name = "dimensoes.html"
    # model = Dimension
    model = Processo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processos = Processo.objects.all()
        context["processos"] = processos
        return context


class Processos(LoginRequiredMixin, ListView):
    template_name = "processos.html"
    model = Processo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["processos"] = Processo.objects.all()
        return context

class ProcessosPorDimensao(LoginRequiredMixin, ListView):
    template_name = "processospordimensao.html"
    model = Processo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dimensao = self.kwargs.get('pk')
        processos_dimensao = Processo.objects.filter(dimension_id=dimensao)
        context["processos_dimensao"] = processos_dimensao
        context["dm"] = dimensao
        return context

class ProcedimentosPorProcesso(LoginRequiredMixin, ListView):
    template_name = "procedimentosporprocesso.html"
    model = Procedimento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processo = self.kwargs.get('pk')
        dimensao = self.kwargs.get('dm')
        print(f" kwargs = {self.kwargs}")
        procedimento_processo = Procedimento.objects.filter(processo_id=processo)
        context["procedimentos_processo"] = procedimento_processo
        context["dimensao"] = dimensao
        context["processo"] = processo
        return context


class EditarProcedimento(View, LoginRequiredMixin):
    template_name = "editarprocedimento.html"

    def get(self, request, **kwargs):
        processo = self.kwargs.get('pk')
        dimensao = self.kwargs.get('dm')
        procedimentos_processo = Procedimento.objects.filter(processo_id=processo)
        LISTA_SITUACAO = [('SIM', 'Sim'), ('EmP', 'Em parte'), ('NAO', 'Não')]
        context = {
            'procedimentos_processo': procedimentos_processo,
            'LISTA_SITUACAO': LISTA_SITUACAO,
            'dimensao': dimensao,
            'processo_id': processo,
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        dimensao = self.kwargs.get('dm')
        processo = self.kwargs.get('pk')
        procedimentos_processo = Procedimento.objects.filter(processo_id=processo)
        lista_novasituacao = request.POST.getlist('atendida')
        for procedimento, situacao in zip(procedimentos_processo, lista_novasituacao):
            procedimento.atendida = situacao
            procedimento.save()
        return redirect(reverse('grc:procedimentosporprocesso', args=[dimensao, processo]))


class Procedimentos(LoginRequiredMixin, ListView):
    template_name = "procedimentos.html"
    model = Procedimento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["procedimentos"] = Procedimento.objects.all()
        context["processos"] = Processo.objects.all().prefetch_related('procedimento')
        return context



class Editarproc2(LoginRequiredMixin, View):     # inutil
    template_name = 'editarprocpage2.html'
    form_class = EditarAtenderForm

    def get_context_data(self):
        context = {}
        context['procedimentos'] = Procedimento.objects.all()
        context['situacao_atual'] = [procedimento.atendida for procedimento in context['procedimentos']]
        context['LISTA_SITUACAO'] = [('SIM', 'Sim'), ('EmP', 'Em parte'), ('NAO', 'Não')]
        context['form'] = self.form_class
        return context

class Editarproc(LoginRequiredMixin, FormView):  # inutil
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


class CriarPlano(LoginRequiredMixin, FormView):
    template_name = "criarplano.html"
    model = Plano
    form_class = CriarPlanoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('tarefa_id')
        plano = Plano.objects.filter(pk=pk)
        context["plano"] = plano
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('grc:planos')


class EditarPlano(LoginRequiredMixin, UpdateView):
    template_name = "editarplano.html"
    model = Plano
    fields = "__all__"
    context_object_name = 'plano'

    def get_object(self, queryset=None):
        plano = None
        pk = self.kwargs.get(self.pk_url_kwarg)
        if id is not None:
            plano = Plano.objects.filter(pk=pk).first()
        return plano

    def get_success_url(self):
        return reverse('grc:planos')

class VerificaTarefasPlano(LoginRequiredMixin, TemplateView):
    template_name = "verificatarefasplano.html"
    model = Tarefa

    def get(self, request, pk):
        plano = get_object_or_404(Plano, pk=pk)
        tarefas_plano = Tarefa.objects.filter(plano=plano)
        if tarefas_plano.exists():
            return render(request, self.template_name, {'tarefas_plano': tarefas_plano})
        else:
            return redirect('grc:excluirplano', pk=pk)



class ExcluirPlano(LoginRequiredMixin, DeleteView):
    template_name = "excluirplano.html"
    model = Plano
    context_object_name = 'plano'
    success_url = reverse_lazy('grc:planos')


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


class Tarefas(LoginRequiredMixin, ListView):
    template_name = "tarefas.html"
    model = Tarefa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano = self.kwargs.get('id')
        tarefas_plano = Tarefa.objects.filter(plano=plano)
        context["tarefas_plano"] = tarefas_plano
        return context



class EditarTarefa(LoginRequiredMixin, UpdateView):
    template_name = "editartarefa.html"
    model = Tarefa
    fields = "__all__"
    context_object_name = 'tarefa'

    def get_object(self, queryset=None):
        tarefa = None
        pk = self.kwargs.get(self.pk_url_kwarg)

        if id is not None:
            tarefa = Tarefa.objects.filter(pk=pk).first()
        return tarefa

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

class ExcluirTarefa(LoginRequiredMixin, DeleteView):
    template_name = "excluirtarefa.html"
    model = Tarefa
    context_object_name = 'tarefa'
    success_url = reverse_lazy('grc:planos')