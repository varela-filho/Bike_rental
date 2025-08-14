from django.shortcuts import render
from django.http import JsonResponse
from .services.previsao_service import prever_alugueis

# Create your views here.
def index(request):
    return render(request, 'galeria/index.html')

def prever(request):
    if request.method == 'POST':
        data_str = request.POST.get('data')
        try:
            previsao, margem_erro = prever_alugueis(data_str)
            return JsonResponse({
                'previsao': int(previsao),
                'margem_erro': int(margem_erro)
            })
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
        
    return JsonResponse({'erro': 'Método não permitido'}, status=405)