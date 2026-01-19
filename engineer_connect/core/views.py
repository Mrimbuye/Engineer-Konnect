from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Engineer Connect is live 🚀</h1>")
