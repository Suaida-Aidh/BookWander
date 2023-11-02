from django.urls import path
from . import views

urlpatterns = [
    
    path('shop/',views.shop, name='shop'),
    path('shop/<int:id>/',views.category_filter, name='shop-by-category'),
    path('category/<slug:product_slug>' , views.product_detail, name = 'single_product'),
    path('search/',views.search, name='search'),


   
    
]