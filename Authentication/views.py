from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import RegistrationalForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Account
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Account
from .forms import UserForm,UserProfileForm



#VERIFICATION IMPORTS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage 


from . models import UserProfile 
from order.models import Order


# Create your views here.

# HOME PAGE
def Home(request):
    
    return render (request,'User/home.html')

#ABOUT PAGE
def about(request):
    
    return render (request,'User/about.html')

#CONTACT PAGE
def contact(request):
    print('aaaaaaaaaaaaaaaaaaaa')
    return render(request, 'User/contact.html')





# LOGIN PAGE
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


# REGISTER PAGE
def Register(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        email = ""  # Define email variable outside the if block

        if request.method == 'POST':
            form = RegistrationalForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
                user.phone_number = phone_number
                user.save()

                # USER ACTIVATION
                current_site = get_current_site(request)
                mail_subject = 'ACTIVATION CODE FROM BOOK WANDER'
                message = render_to_string('authentication/account_verification_email.html', {
                    'first_name': first_name,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Registeration successful Please check your given gmail for activation')
                
                return redirect('Login')
        else:
            form = RegistrationalForm()
        context = {
            'form': form
        }

        return render(request, 'Authentication/register.html', context)


#  LOGOUT CONDITION 
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('Home')



#EMAIL_ACTIVARTION CONDITION
def activate (request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations Your account is activated ')
        return redirect('Login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('Register') 





# USER PROFILE

# MYACCOUNT CONDITION (DASH BOARD)
@login_required(login_url='signin')
def user_profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders_count = orders.count()
    userprofile = UserProfile.objects.filter(user=request.user)

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile
    }

    return render(request, 'User/user_profile.html', context)




# EDIT PROFILE CONDITION
@login_required(login_url='signin')
def edit_profile(request):
    if UserProfile.objects.filter(user=request.user):
        userprofile = get_object_or_404(UserProfile, user=request.user)
    else: 
        userprofile = UserProfile.objects.create(user=request.user)   
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() 
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect(edit_profile)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form'   : user_form,
        'profile_form': profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'User/edit_profile.html', context)
