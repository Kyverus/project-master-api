from django.shortcuts import HttpResponse

def home_page(request):
    return HttpResponse("THIS IS THE PROJECT MANAGER API")