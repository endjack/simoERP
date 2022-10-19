from django.http.response import HttpResponse
from financeiro.models import NotaCompleta
import json

validar_item_nota = {'descricao' : False, 'qtd': False, 'valor': False}
validar_descricao_nota = {'data_emissao': False, 'centro_de_custo': False, 'itens_nota': False}


def check_data_emissao(request):
    global validar_descricao_nota
    if request.method == 'POST':
        field = request.POST.get('data_emissao')      
        
        if not field or field == "":  
            validar_descricao_nota['data_emissao'] = False
            response =  HttpResponse('Data inválida')
            response['HX-Trigger'] = json.dumps({'errorDataEmissao': True, 'disableButtonNotaCompleta': True })
            return response
        else:
            validar_descricao_nota['data_emissao']  = True
            response =  HttpResponse(status=200)
            response['HX-Trigger'] = 'okDataEmissao'
            # print(validar_descricao_nota.values())
            if all(validar_descricao_nota.values()):
                response['HX-Trigger'] = json.dumps({'okDataEmissao': True, 'enableButtonNotaCompleta': True })
            return response
         
def check_centro_de_custo(request):
    global validar_descricao_nota
    if request.method == 'POST':
        field = request.POST.get('centro_de_custo')      
        
        if not field or field == "":  
            validar_descricao_nota['centro_de_custo'] = False
            response =  HttpResponse('Centro de Custo inválido')
            response['HX-Trigger'] = json.dumps({'errorCentrodeCusto': True, 'disableButtonNotaCompleta': True})
            return response
        else:
            validar_descricao_nota['centro_de_custo'] = True
            response =  HttpResponse(status=200)
            response['HX-Trigger'] = 'okCentrodeCusto'
            # print(validar_descricao_nota.values())
            if all(validar_descricao_nota.values()):
                response['HX-Trigger'] = json.dumps({'okCentrodeCusto': True, 'enableButtonNotaCompleta': True})
            return response
        
def check_qtd_itens_conta(request):
    global validar_descricao_nota
    from .views import id_nota_em_processo
    if request.method == 'GET':
        nota = NotaCompleta.objects.get(pk = int(id_nota_em_processo))
        if not nota:
            validar_descricao_nota['itens_nota'] = False
            response =  HttpResponse('')
            response['HX-Trigger'] = json.dumps({'errorItensNota': True, 'disableButtonNotaCompleta': True})
            return response
        else:
            if nota.itens.all().count() > 0:
                validar_descricao_nota['itens_nota'] = True
                response =  HttpResponse(status=200)
                response['HX-Trigger'] = 'okItensNota'
                print(validar_descricao_nota.values())
                if all(validar_descricao_nota.values()):
                    response['HX-Trigger'] = json.dumps({'okItensNota': True, 'enableButtonNotaCompleta': True})
                return response
            else:
                validar_descricao_nota['itens_nota'] = False
                response =  HttpResponse('')
                response['HX-Trigger'] = json.dumps({'errorItensNota': True, 'disableButtonNotaCompleta': True})
                return response

            
def check_descricao_item_conta(request):
    global validar_item_nota
    if request.method == 'POST':
        field = request.POST.get('descricao')
        
        if not field or len(field) <3:
            validar_item_nota['descricao'] = False
            response = HttpResponse('Descrição precisa ter no mínimo 3 caracteres')
            response['HX-Trigger'] = 'disableButton'
            return response  
        else:
            validar_item_nota['descricao'] = True
            response =  HttpResponse(status=200)
            if all(validar_item_nota.values()):
                response['HX-Trigger'] = 'enableButton'
            return response
        
def check_quantidade_item_conta(request):
    global validar_item_nota
    if request.method == 'POST':
        field = request.POST.get('qtd')
        
        if not field or float(field) <= 0:
            validar_item_nota['qtd'] = False
            response = HttpResponse('Quantidade Inválida')
            response['HX-Trigger'] = 'disableButton'
            return response
        else:
            validar_item_nota['qtd'] = True
            response =  HttpResponse(status=200)
            if all(validar_item_nota.values()):
                response['HX-Trigger'] = 'enableButton'
            return response
        
def check_valor_item_conta(request):
    global validar_item_nota
    if request.method == 'POST':
        field = request.POST.get('valor')
        
        if not field or field == '' or float(field.replace(".","").replace(",",".")) <= 0 :
            validar_item_nota['valor'] = False
            response = HttpResponse('Valor Inválido')
            response['HX-Trigger'] = 'disableButton'
            return response
        else:
            validar_item_nota['valor'] = True
            response =  HttpResponse(status=200)
            if all(validar_item_nota.values()):
                response['HX-Trigger'] = 'enableButton'
            return response
    
        