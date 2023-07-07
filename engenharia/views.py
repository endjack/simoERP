from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def home_engenharia(request, template_name = 'engenharia/home.html'):
    """
    Retorna a página inicial do financeiro
    """
    date = datetime.now()
    
    if request.method == 'GET':
             
        context = {
            'date': date,
        }

        
        return render(request, template_name , context)
        
