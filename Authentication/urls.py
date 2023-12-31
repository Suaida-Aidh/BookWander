
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.Home, name='Home'),
    path('login/', views.Login , name='Login'),
    path('register/', views.Register , name='Register'),
    path('signout/', views.signout, name="signout"),

    # ACTIVATION URLS IN EMIAL
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

    # USER PROFILE
    path('user_profile/', views.user_profile, name = 'user_profile'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),

    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name ='contact'),
    


]