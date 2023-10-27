from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.dashboard, name='dashboard'),
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

   


]