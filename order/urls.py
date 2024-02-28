
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('place-order/', views.placeorder, name = 'place_order'),  
    path('my-orders/', views.myorder, name = 'myorder'),
    path('view-order/<str:t_no>', views.vieworder, name = 'view_order'),
    path('cancel_order/<str:t_no>', views.Cancel_order, name ='cancel_order'),
    path('proceed-to-pay/',views.razorpaycheck , name='proceed-to-pay'),
    path('return_order/<str:t_no>', views.return_order, name='return_order'),

    path('addresses/', views.addresses, name='addresses'),
    path('add_address/', views.add_address, name='add_address'),  # Define the URL pattern for add_address view
    path('select_address/', views.select_address, name='select_address'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)