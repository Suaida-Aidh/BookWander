from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from cart.models import CartItem
from Authentication.models import Account
from .models import Profile
from .models import Order, OrderItem , Wallet, Transaction
from store.models import Product
import random
from django.contrib import messages
from cart.models import Cart
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Authentication.models import Account


@never_cache
@login_required(login_url=('Login'))
def placeorder(request):
    print(request.POST)
    if request.method == 'POST':

        # cart check
        cart_items = CartItem.objects.filter(user=request.user.id)
        if not cart_items:
            return redirect('shop')

        currentuser = Account.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:  # type: ignore
            currentuser.first_name = request.POST.get(
                'first_name')  # type: ignore
            currentuser.last_name = request.POST.get(
                'last_name')  # type: ignore
            currentuser.save()  # type: ignore
            print(currentuser.first_name)  # type: ignore

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        newOrder = Order()
        newOrder.user = request.user
        newOrder.first_name = request.POST.get('first_name')
        newOrder.last_name = request.POST.get('last_name')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.address = request.POST.get('address')
        newOrder.city = request.POST.get('city')
        newOrder.state = request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pincode = request.POST.get('pincode')
        newOrder.payment_mode = request.POST.get('payment_mode')
        newOrder.payment_id = request.POST.get('payment_id')

        # taking total price
        cart_items = CartItem.objects.filter(user=request.user)
        total = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)

        newOrder.total_price = total
        trackNo = 'Bookwander'+str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackNo) is None:
            trackNo = 'Bookwnader'+str(random.randint(1111111, 9999999))
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
            # TO DECRESE THE QUANTITY OF PRODUCT
            orderproduct = Product.objects.filter(
                id=item.product_id).first()  # type: ignore
            orderproduct.stock -= item.quantity  # type: ignore
            orderproduct.save()  # type: ignore

        # TO CLEAR THE USER'S CART
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, 'Order Placed Successfully')

    payMode = request.POST.get('payment_mode')
    if (payMode == "Paid by Razorpay"):

        return JsonResponse({'status': "Your order has been placed successfully"})

    elif (payMode == "COD"):
        return redirect('my_order')
    return redirect('my_order')


# MY ORDER FUNCTION
@never_cache
@login_required(login_url='signin')
def myorder(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders,
    }
    return render(request, 'User/my_order.html', context)


@never_cache
@login_required(login_url=('signin'))
def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no, user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'orderitems': orderitems,

    }
    return render(request, 'User/view_order.html', context)


def Cancel_order(request, t_no):
    order = Order.objects.get(tracking_no=t_no, user=request.user)

    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()

        # Retrieve or create the user's wallet
        wallet , _= Wallet.objects.get_or_create(user=request.user)
        print("wallet")
        print(wallet)

        # Add the order amount back to the wallet balance
        wallet.balance += order.total_price
        wallet.save()

        # Create a transaction record for the refund
        Transaction.objects.create(wallet=wallet, transaction_type='Refund', amount=order.total_price)

    return redirect('my_order')


@never_cache
@login_required(login_url=('Login'))  # type: ignore
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = 0
    if cart:

        for item in cart:
            total_price += (item.product.price * item.quantity)

        total_price += (6 * total_price)/100

        return JsonResponse({'total_price': int(total_price)})
    else:
        return redirect('shop')
