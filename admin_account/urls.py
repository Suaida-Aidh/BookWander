from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.dashboard, name='admin_dashboard'),
    # product management
    path('product_list/',views.product_management, name='product_list'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    

    #USER MANAGEMENT
    path('user_managemnet/',views.user_management,name="user_management"),
    path('block_user/<int:user_id>/',views.block_user,name="block_user"),
    path('unblock_user/<int:user_id>/',views.unblock_user,name="unblock_user"),

    #CATEGORY MANAGEMENT
    path('category_management/', views.category_management, name="category_management"),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name="edit_category"),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),

    #ORDER MANAGEMENT
    path('order_management/', views.order_management, name="order_management"),
    path('manager_vieworder/<str:tracking_no>/', views.manager_vieworder, name='manager_vieworder'),
    path('manager_accept_order/<str:tracking_no>/', views.manager_accept_order, name='manager_accept_order'),
    path('manager_ship_order/<str:tracking_no>/', views.manager_ship_order, name='manager_ship_order'),
    path('manager_delivered_order/<str:tracking_no>/', views.manager_delivered_order, name='manager_delivered_order'),
    path('manager_cancel_order/<str:tracking_no>/', views.manager_cancel_order, name='manager_cancel_order'),


    #MULTIPLE IMAGE MANAGEMENTS
    path('multiple_image_management/',views.multiple_image_management,name='multiple_image_management'),


   


]