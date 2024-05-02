from django.core.cache import cache
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template.loader import render_to_string
from simo import settings
import pdfkit
import os



@csrf_exempt
def limpar_cache(request):  
    cache.clear()
    print("------------> CACHE LIMPO <-------------")
    return HttpResponse()

@csrf_exempt
def gerar_pdf_by_template(template_name, context, filename='file', type='view'):        
        
        html = render_to_string(template_name, context)
        
        #CSS
        css = os.path.join(settings.PROJECT_ROOT, 'static/css', 'bootstrap.min.css')
        
        #renderizando PDF
        options={
            'page-size':'Letter',
            'encoding' : 'UTF-8',
            "enable-local-file-access": None,  
            # 'javascript-delay':'5000',   
        }

        pdf = pdfkit.from_string(html, css=css, options=options)

        
        if pdf:
            response= HttpResponse(pdf, content_type='application/pdf')
      
            if type == "view":
                response['Content-Disposition']= "inline; filename= %s" %(filename) #visualizar
            else:   
                response['Content-Disposition']= "attachment; filename= %s" %(filename) #download
            return response
        return HttpResponse("Page Not Found")  


# @csrf_exempt
# def handler404(request, exception, template_name='404.html'):
#     response = render(request, template_name, status=404)
#     response.status_code = 404
#     return response