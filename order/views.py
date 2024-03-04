from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from cart.models import CartItem
from .models import Order, OrderItem , Wallet, Transaction , Address
from store.models import Product
import random
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddressForm
from django.shortcuts import get_object_or_404
from decimal import Decimal




@never_cache
@login_required(login_url=('Login'))
def placeorder(request):
    if request.method == 'POST':


        # Fetch selected billing address
        billing_address_id = request.POST.get('billing_address')
        billing_address = get_object_or_404(Address, id=billing_address_id)
        print(billing_address,billing_address_id,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        
        # Fetch payment mode and payment id
        payment_mode = request.POST.get('payment_mode')
        payment_id = request.POST.get('payment_id')

        # Calculate total price
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

        # Create the order
        new_order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            phone=billing_address.phone,  # Assuming this is a field in your User model
            address=billing_address.address,
            city=billing_address.city,
            state=billing_address.state,
            country=billing_address.country,
            pincode=billing_address.pincode,
            total_price=total_price,
            payment_mode=payment_mode,
            payment_id=payment_id,
            multiple_address=billing_address
        )

        # Generate tracking number
        track_no = 'Bookwander' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'Bookwander' + str(random.randint(1111111, 9999999))
        new_order.tracking_no = track_no
        new_order.save()

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                user=request.user
            )
            # Decrease product stock
            order_product = Product.objects.get(id=item.product_id)
            order_product.stock -= item.quantity
            order_product.save()

        # Clear the user's cart
        CartItem.objects.filter(user=request.user).delete()

        messages.success(request, 'Order Placed Successfully')

        # Redirect or return JSON response based on payment mode
        if payment_mode == "Paid by Razorpay":
                return JsonResponse({'status': "Your order has been placed successfully"})
        elif payment_mode == "COD" :
            return redirect('myorder')
        return redirect('myorder')
        



# MY ORDER FUNCTION
@never_cache
@login_required(login_url='Login')
def myorder(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    

    for order in orders:
        total = 0
        for item in order.orderitem_set.all():  # Assuming you have an OrderItem model related to Order
            total += (item.product.price * item.quantity)
        shipping = Decimal('0.06') * total  # Calculate shipping charges
        order.total_price = total + shipping
        order.shipping_charges = shipping  # Save shipping charges to order object
        order.save()  # Save the updated total price and shipping charges to the database
        
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
@login_required(login_url=('Login'))
def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no, user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    address = Order.objects.filter(user=request.user).first()  # Fetch associated address
    print(order.multiple_address.first_name)
    print(order.multiple_address.address)
    context = {
        'order': order,
        'orderitems': orderitems,
        'address': address,  # Pass the address object to the context
    }
    return render(request, 'User/view_order.html', context)


def addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'User/add_address.html', {'addresses':addresses})


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')  # Redirect to some view after adding the address
    else:
        form = AddressForm()
    
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'User/add_address.html', {'form': form, 'addresses': addresses})

def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    address.delete()
    print('deleeeeeeeeeeeeeeeeeeeeeeeeeeeteeeeeetttttttttt')
    return redirect('checkout')


def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('checkout')  # Redirect back to add_address view after editing
    else:
        form = AddressForm(instance=address)
    return render(request, 'User/edit_address.html', {'form': form, 'address': address})

def select_address(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        if selected_address_id:
            selected_address = Address.objects.get(id=selected_address_id)
            request.session['selected_address_id'] = selected_address_id
            return redirect('checkout')

    addresses = Address.objects.all()
    return render(request, 'User/checkout.html', {'addresses': addresses})

def Cancel_order(request, t_no):
    order = Order.objects.get(tracking_no=t_no, user=request.user)

    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()

        # Credit stock for each item in the order
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            print(f"Before credit: Product {product.id} - Stock: {product.stock}")
            product.stock += item.quantity  # Increase the stock quantity
            product.save()
            print(f"After credit: Product {product.id} - Stock: {product.stock}")
            


        # Retrieve or create the user's wallet
        wallet , _= Wallet.objects.get_or_create(user=request.user)
        print("wallet")
        print(wallet)

        # Add the order amount back to the wallet balance
        wallet.balance += order.total_price
        wallet.save()

    

        # Create a transaction record for the refund
        Transaction.objects.create(wallet=wallet, transaction_type='Refund', amount=order.total_price)

    return redirect('myorder')




def return_order(request, t_no):
    order = Order.objects.get(tracking_no=t_no, user=request.user)

    if order.status == 'Delivered':
        # Calculate refund amount (for demonstration purposes, assuming full refund)
        refund_amount = order.total_price

        # Update order status to indicate it's returned
        order.status = 'Returned'
        order.save()
        
        # Credit stock for each item in the order
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            product.stock += item.quantity  # Increase the stock quantity
            product.save()
        # Retrieve or create the user's wallet
        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        # Add the refund amount back to the wallet balance
        wallet.balance += refund_amount
        wallet.save()

        # Create a transaction record for the refund
        Transaction.objects.create(wallet=wallet, transaction_type='Refund', amount=refund_amount)

    return redirect('myorder')

@never_cache
@login_required(login_url=('Login'))  # type: ignore
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = 0
    if cart:

        for item in cart:
            total_price += (item.product.price * item.quantity)

        total_price += (6 * total_price)/100

        return JsonResponse({'total_price': (total_price)})
    else:
        return redirect('shop')
