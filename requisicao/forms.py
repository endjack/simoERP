from django.conf import settings
from django.db.models import fields
from django.forms.models import inlineformset_factory
from requisicao.models import ItemRequisicao, Requisicao
from django.forms import ModelForm, HiddenInput, DateInput, forms

class GerarRequisicaoForm(ModelForm):
    #data = fields.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Requisicao
        fields = ['obra','local','solicitante','almoxarife','data']
        #widgets={'data': HiddenInput()}

class ItemRequisicaoForm(ModelForm):
    class Meta:
        model = ItemRequisicao
        fields = ['item', 'quantidade']


ItemRequisicaoFormSet = inlineformset_factory(Requisicao, ItemRequisicao,
                                            form=ItemRequisicaoForm, extra=3)