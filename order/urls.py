from django.urls import path
from .import views

urlpatterns = [

    path('place-order/', views.placeorder, name = 'place_order'),  
    path('my-orders/', views.myorder, name = 'my_order'),
    path('view-order/<str:t_no>', views.vieworder, name = 'view_order'),
    path('cancel_order/<str:t_no>', views.Cancel_order, name ='cancel_order'),

    path('proceed-to-pay',views.rezorpaycheck , name='proceed-to-pay'),

]