from django.urls import path
from . import views



urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_cart/<int:product_id>/',views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name='remove_cart'),
    path('checkout/',views.checkout, name='checkout'),

    # wishlist
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('cart/delete-from-wishlist/<int:product_id>/', views.delete_from_wishlist, name='delete_from_wishlist'),
    path('delete-from-wishlist/<int:product_id>/',views.delete_from_wishlist, name="delete_from_wishlist"),
    path('wishlist/',views.wishlist, name="wishlist"),
    # path('cart/delete-from-wishlist/<int:product_id>/', views.delete_from_wishlist, name='delete_from_wishlist'),
    # path('cart/wishlist/', views.wishlist, name='wishlist'),

   
]