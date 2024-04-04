
from django import  forms
from .models import Procedimento, LISTA_SITUACAO, Tarefa, Plano
from django.forms import modelform_factory, ModelForm, widgets


EditarProcedimentoForm = modelform_factory(
    model=Procedimento,
    fields=['atendida']
)




#
# class ErrorHandlingHiddenInput(widgets.HiddenInput):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.error_messages = {
#             'incomplete': 'Este campo é obrigatório.',
#         }
#
# class EditarProcedimentoForm(forms.Form):
#     nova_situacao = forms.MultiValueField(
#         fields=(
#             ErrorHandlingHiddenInput(attrs={'class': 'nic-input'}),
#             ErrorHandlingHiddenInput(attrs={'class': 'nova-situacao-input'}),
#         ),
#         required=False,
#     )
#
#


# class EditarProcedimentoForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["nova_situacao"] = forms.ChoiceField(
#             choices=LISTA_SITUACAO,
#             widget=forms.Select(attrs={'class': 'text-black '}),
#         )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         novas_situacoes = {}
#         for key, value in self.cleaned_data.items():
#             if key.startswith("procedimento_"):
#                 nic = key.split("_")[1]
#                 novas_situacoes[nic] = value
#         cleaned_data["nova_situacao"] = novas_situacoes
#         return cleaned_data
#



# class EditarProcedimentoForm(forms.Form):
#     nova_situacao = forms.ChoiceField(
#         choices=LISTA_SITUACAO)



EditarAtenderForm = modelform_factory(
    model=Procedimento,
    fields=['atendida'],
)

# class EditarAtenderForm(forms.ModelForm):
#     class Meta:
#         model = Procedimento
#         fields = ['atendida']
#
#     def __init__(self, *args, **kwargs):
#         self.procedimentos = kwargs.pop('procedimentos')
#
#         super().__init__(*args, **kwargs)
#         for procedimento in self.procedimentos:
#             self.fields[f'atendida_{procedimento.pk}'] = forms.ChoiceField(choices=LISTA_SITUACAO, required=False)


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
