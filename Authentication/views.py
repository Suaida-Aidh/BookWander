from django.shortcuts import render,HttpResponse
from .forms import RegistrationalForm
from .models import Account
# Create your views here.

def Home(request):
    return render (request,'User/home.html')


def Login(request):
    return render (request,'Authentication/login.html')

def Register(request):
    if request.method == 'POST':
        form = RegistrationalForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationalForm()
    context={
        'form':form,

    }

    

    return render (request,'Authentication/register.html',context)