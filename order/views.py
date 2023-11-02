# from django.shortcuts import redirect, JsonResponse, messages
# import random

# @never_cache
# @login_required(login_url=('signin'))
# def placeorder(request):
#     if request.method == 'POST':

#         # cart check
#         cart_items = CartItem.objects.filter(user=request.user.id)
#         if not cart_items:
#             return redirect('store')

#         currentuser = Account.objects.filter(id=request.user.id).first()
#         if not currentuser.first_name:
#             currentuser.first_name = request.POST.get('first_name')
#             currentuser.last_name = request.POST.get('last_name')
#             currentuser.save()

#         if not Profile.objects.filter(user=request.user):
#             userprofile = Profile()
#             userprofile.user = request.user
#             userprofile.phone = request.POST.get('phone')
#             userprofile.address = request.POST.get('address')
#             userprofile.city = request.POST.get('city')
#             userprofile.state = request.POST.get('state')
#             userprofile.country = request.POST.get('country')
#             userprofile.pincode = request.POST.get('pincode')
#             userprofile.save()

#         newOrder = Order()
#         newOrder.user = request.user
#         newOrder.first_name = request.POST.get('first_name')
#         newOrder.last_name = request.POST.get('last_name')
#         newOrder.email = request.POST.get('email')
#         newOrder.phone = request.POST.get('phone')
#         newOrder.address = request.POST.get('address')
#         newOrder.city = request.POST.get('city')
#         newOrder.state = request.POST.get('state')
#         newOrder.country = request.POST.get('country')
#         newOrder.pincode = request.POST.get('pincode')
#         newOrder.payment_mode = request.POST.get('payment_mode')
#         newOrder.payment_id = request.POST.get('payment_id')

#         # taking total price
#         cart_items = CartItem.objects.filter(user=request.user)
#         total = 0
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)

#         newOrder.total_price = total
#         trackNo = 'eyebrow' + str(random.randint(1111111, 9999999))
#         while Order.objects.filter(tracking_no=trackNo).exists():
#             trackNo = 'eyebrow' + str(random.randint(1111111, 9999999))
#         newOrder.tracking_no = trackNo
#         newOrder.save()

#         newOrderItems = CartItem.objects.filter(user=request.user)
#         for item in newOrderItems:
#             OrderItem.objects.create(
#                 order=newOrder,
#                 product=item.product,
#                 price=item.product.price,
#                 quantity=item.quantity,
#                 user=request.user
#             )
#             # TO DECREASE THE QUANTITY OF PRODUCT
#             orderproduct = Product.objects.filter(id=item.product_id).first()
#             orderproduct.stock -= item.quantity
#             orderproduct.save()

#         # TO CLEAR THE USER'S CART
#         CartItem.objects.filter(user=request.user).delete()

#         messages.success(request, 'Order Placed Successfully')

#         payMode = request.POST.get('payment_mode')
#         if payMode == "Paid by Razorpay":
#             return JsonResponse({'status': "Your order has been placed successfully"})
#         elif payMode == "COD":
#             return redirect('myorder')
#     return redirect('checkout')

