from django.shortcuts import HttpResponse,render

def index(request):
    return render(request,"main.html")