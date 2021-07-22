from django import forms
from django.forms import models
from .models import *


class InserirObraForm(forms.ModelForm):  
    class Meta:
        model = Obra
        fields = '__all__'



class InserirLocalForm(forms.ModelForm):  
    class Meta:
        model = Local
        fields = '__all__'