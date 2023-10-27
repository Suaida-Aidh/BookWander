from django.shortcuts import render,get_object_or_404,redirect
from .models import Category_list, Product, Authors
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductImage
from order.models import OrderItem
from cart.models import CartItem,WishlistItem
from cart.views import _cart_id

# Create your views here.


def shop (request,category_slug=None ):
    categories=Category_list.objects.all()
    products = None
    if category_slug != None:
        categories =get_object_or_404(Category_list,slug=category_slug)
        products= Product.objects.filter(category=categories,is_available =True).order_by('-created_date')
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count =products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('-created_date')
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count= products.count()


    context =  {
        'products': paged_products, 
        'products_count':products_count,
        'categories' : categories,
    }
    return render(request, 'User/shop.html', context)

def category_filter(request, id):
    try:
        products = Product.objects.filter(category__id=id,is_available =True).order_by('-created_date')
        categories = Category_list.objects.all()
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count =products.count()
        context =  {
        'products': paged_products, 
        'products_count':products_count,
        'categories' : categories,
    }
        return render(request, 'User/shop.html', context)
    except:
        return redirect(shop)
    


def product_detail(request,product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        multiple_images = ProductImage.objects.filter(product=single_product)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    try:
        orderitem=None
        if request.user.is_authenticated:
         orderitem =  OrderItem.objects.filter(user=request.user,product_id=single_product.id).exists()  # type: ignore
    except OrderItem.DoesNotExist:
        orderitem = None 

    #showing the old reviews
    
    wishlist=None
    if request.user.is_authenticated:
        wishlist= WishlistItem.objects.filter(product=single_product)
    

    context = {
        'single_product' : single_product,
        'in_cart'        : in_cart,
        'multiple_images': multiple_images,
        'orderitem'      : orderitem,
        
        'wishlist'       : wishlist
        }           
    return render (request,'User/single_product.html',context)

