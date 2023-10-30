from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegistrationalForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Account
from django.contrib.auth.decorators import login_required
# Create your views here.

def Home(request):
    
    return render (request,'User/home.html')


def Login(request):
    if request.user.is_authenticated:
        return redirect('Home')
    
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('Home')
                else:
                    messages.error(request, 'Invalid login credentials.')
        else:
            form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'Authentication/login.html', context)

def Register(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        if request.method == 'POST':
            form = RegistrationalForm(request.POST)
            if form.is_valid():
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                phone_number=form.cleaned_data['phone_number']
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,  password=password)
                user.phone_number = phone_number
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('Login')
        else:
            form = RegistrationalForm()
        context={
            'form':form
        }
        return render (request,'Authentication/register.html',context)



#  LOGOUT CONDITION 
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('Home')