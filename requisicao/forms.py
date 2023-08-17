from django.forms.models import inlineformset_factory
from requisicao.models import ItemRequisicao, Requisicao
from django.forms import ModelForm

class ObraRequisicaoForm(ModelForm):
    class Meta:
        model = Requisicao
        fields = ['obra', 'local']

class ItemRequisicaoForm(ModelForm):
    class Meta:
        model = ItemRequisicao
        fields = ['item', 'quantidade']


ItemRequisicaoFormSet = inlineformset_factory(Requisicao, ItemRequisicao,
                                            form=ItemRequisicaoForm, extra=3)