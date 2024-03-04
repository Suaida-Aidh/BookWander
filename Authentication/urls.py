
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Authentication\password_reset_form.html'), name ='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='Authentication\password_reset_done.html'), name ='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Authentication\password_reset_confirm.html'), name ='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Authentication\password_reset_complete.html'), name ='password_reset_complete'),

    path('ChangePassword/', views.Change_Password, name ='ChangePassword'),



]