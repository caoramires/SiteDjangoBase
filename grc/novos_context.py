from .models import Framework, Dimension, Processo, Procedimento

def lista_dimensoes(request):
    lista_dimensoes = Dimension.objects.all()

    return {"lista_dimensoes": lista_dimensoes}

def lista_processos(request):
    lista_processos = Processo.objects.all()

    return {'lista_processos': lista_processos}

def lista_procedimentos(request):
    lista_procedimentos = Procedimento.objects.all()

    return {'lista_procedimentos': lista_procedimentos}

def proc_por_dimensao(request):
    proc_por_dimensao = Dimension.objects.all().prefetch_related('processo')

    return {'proc_por_dimensao': proc_por_dimensao}

