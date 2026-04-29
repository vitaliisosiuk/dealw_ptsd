from django.shortcuts import render

# Create your views here.

def welcome_page(request):
    return render(request, "core/index.html")

def ptsd_info(request):
    return render(request, "core/ptsdinfo.html")
