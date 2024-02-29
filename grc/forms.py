from django import forms

class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)

