from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product
from cart.models import CartItem, Cart
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request, total=0, quantity=0, cart_items=None):
    shipping = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        shipping = (8 * total) / 100
        grand_total = total + shipping
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping': shipping,
        'grand_total': grand_total,
    }

    return render(request, 'User/cart.html', context)

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        # If user is authenticated, add the product to the cart
        cart_item, created = CartItem.objects.get_or_create(product=product, user=current_user)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # If user is not authenticated, add the product to the cart using session
        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        try:
            # Try to get an existing cart item for the same product
            cart_item = CartItem.objects.get(product=product, cart=cart)
            # If it exists, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            # If it doesn't exist, create a new cart item with a quantity of 1
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)

    return redirect('cart')





#REMOVE CART ITEM
def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
           cart_item    = CartItem.objects.get(product=product,user=request.user, id=cart_item_id)
        else:
           cart    = Cart.objects.get(cart_id=_cart_id(request))
           cart_item    = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save() 
        else:
         cart_item.delete()
    except:
        pass   
    return redirect ('cart')   


#CHECK OUT CONDITONS 
@login_required(login_url='signin')
def checkout(request,total=0, quantity=0, cart_items=None):
    shipping = 0
    grand_total = 0
    try:
        
        if request.user.is_authenticated:
           cart_items   = CartItem.objects.filter(user=request.user, is_active=True)
        #    userprofile = Profile.objects.filter(user=request.user).first() 
        else:
           cart         = Cart.objects.get(cart_id=_cart_id(request))
           cart_items   = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            shipping = (6 * total)/100
            grand_total   = total+shipping
           
    except ObjectDoesNotExist:
        pass
    context = {
        'total'      : total,
        'quantity'   : quantity,
        'cart_items' : cart_items,
        'shipping': shipping,
        'grand_total': grand_total,
        # 'userprofile': userprofile, #type:ignore 
    }

    return render(request,'User/checkout.html',context)  
