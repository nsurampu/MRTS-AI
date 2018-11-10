from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def admin_portal(request):
    return HttpResponse("lite admin")