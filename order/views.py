from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from cart.models import CartItem
from Authentication.models import Account
from .models import Profile
from .models import Order,OrderItem
from store.models import Product
import random
from django.contrib import messages
from cart.models import Cart
from django.http import JsonResponse

@never_cache
@login_required(login_url=('signin'))
def placeorder(request):
    print('first')
    if request.method == 'POST':

        # cart check
        cart_items = CartItem.objects.filter(user=request.user.id)
        print(request.POST,'aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        if not cart_items:
            return redirect('shop')
        print('second')
        currentuser = Account.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('first_name')
            currentuser.last_name = request.POST.get('last_name')
            currentuser.save()
        print('third')
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('Address')
            userprofile.city = request.POST.get('City')
            userprofile.state = request.POST.get('State')
            userprofile.country = request.POST.get('Country')
            userprofile.pincode = request.POST.get('pincode')
            print('nottt')
            userprofile.save()
            print('savee')

        newOrder = Order()
        newOrder.user = request.user
        newOrder.first_name = request.POST.get('first_name')
        newOrder.last_name = request.POST.get('last_name')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')

        newOrder.address = request.POST.get('Address')  

        newOrder.city = request.POST.get('City')
        newOrder.state = request.POST.get('State')
        newOrder.country = request.POST.get('Country')
        newOrder.pincode = request.POST.get('pincode')
        newOrder.payment_mode = request.POST.get('payment_mode')
        newOrder.payment_id = request.POST.get('payment_id')

        # taking total price
        cart_items = CartItem.objects.filter(user=request.user)
        total = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)

        newOrder.total_price = total
        trackNo = 'Bookwander' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackNo).exists():
            trackNo = 'Bookwander' + str(random.randint(1111111, 9999999))
        newOrder.tracking_no = trackNo
        newOrder.save()

        newOrderItems = CartItem.objects.filter(user=request.user)
        for item in newOrderItems:
            OrderItem.objects.create(
                order=newOrder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                user=request.user
            )
            # TO DECREASE THE QUANTITY OF PRODUCT
            print('fdjfjdf')
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.stock -= item.quantity
            orderproduct.save()

        # TO CLEAR THE USER'S CART
        print('frndjvn')
        CartItem.objects.filter(user=request.user).delete()
        print('bgvjdf')

        messages.success(request, 'Order Placed Successfully')
        print('fhbv')

        payMode = request.POST.get('payment_mode')
        print('orderrrrrrr')
        if payMode == "COD":
            return redirect('my_order')
    return redirect('checkout')



#MY ORDER FUNCTION
@never_cache
@login_required(login_url=('signin')) 
def myorder(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    context ={
        'orders':orders
    }
    return render(request,'User/my_order.html',context)


@never_cache
@login_required(login_url=('signin')) 
def vieworder(request,t_no):
    order =Order.objects.filter(tracking_no=t_no,user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
        
    }
    return render(request,'User/view_order.html',context)



def Cancel_order(request,t_no):
    order =Order.objects.get(tracking_no=t_no,user=request.user)
    order.status ='Cancelled'
    order.save()
    return redirect('my_order')



# razorpay

def rezorpaycheck(request):
    cart = Cart.objects.filter(user = request.user)
    for item in cart:
        total_price = item.total_price * item.quantity
    return JsonResponse({'total_price':total_price})
