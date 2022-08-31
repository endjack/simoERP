from django import forms
from .models import *


class TarefasForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = '__all__'
        exclude = ['usuario',]
