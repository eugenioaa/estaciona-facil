from django.shortcuts import render

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def sistemaAval(request):
     return render(request, "telaAval.html")
