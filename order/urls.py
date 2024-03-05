
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('place_order/new/', views.place_order, name = 'place_order'),  
    path('my-orders/', views.myorder, name = 'myorder'),
    path('view-order/<str:t_no>', views.vieworder, name = 'view_order'),
    path('cancel_order/<str:t_no>', views.Cancel_order, name ='cancel_order'),
    path('proceed-to-pay/',views.razorpaycheck , name='proceed-to-pay'),
    path('return_order/<str:t_no>', views.return_order, name='return_order'),

    path('addresses/', views.addresses, name='addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('select_address/', views.select_address, name='select_address'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)