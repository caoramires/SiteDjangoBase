
from django import  forms
from .models import Procedimento, LISTA_SITUACAO, Tarefa, Plano
# from django.forms import  modelform_factory
#
#
# EditarAtenderForm = modelform_factory(
#     model=Procedimento,
#     fields=['atendida'],
# )
class EditarAtenderForm(forms.ModelForm):
    class Meta:
        model = Procedimento
        fields = ['atendida']

    def __init__(self, *args, **kwargs):
        self.procedimentos = kwargs.pop('procedimentos')

        super().__init__(*args, **kwargs)
        for procedimento in self.procedimentos:
            self.fields[f'atendida_{procedimento.pk}'] = forms.ChoiceField(choices=LISTA_SITUACAO, required=False)


class CriarPlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields ="__all__"



class CriaTarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields ="__all__"

class EditarTarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields ="__all__"
