from django import forms
from obras.models import *

class NomeObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nome']
