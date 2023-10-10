from django.shortcuts import render,HttpResponse
from .forms import RegistrationalForm
# Create your views here.

def Home(request):
    return render (request,'User/home.html')


def Login(request):
    return render (request,'Authentication/login.html')

def Register(request):
    form = RegistrationalForm()
    context={
        'form':form,

    }

    

    return render (request,'Authentication/register.html')