from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from store.models import Product
from django.core.paginator import Paginator
from django.db.models import Q
from .form import ProductForm, MultipleImagesForm
from store.models import MultipleImages
from django.contrib import messages
from Authentication.models import Account
from store.models import Category_list
from order.models import Order, OrderItem
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from datetime import datetime
from datetime import date
from store.models import Coupon, Offer
from django.core.exceptions import ValidationError
import csv
from django.http import HttpResponse
from fpdf import FPDF
from django.db.models import Prefetch
from itertools import groupby


# Create your views here.

@login_required(login_url='Login')
def dashboard(request):

    orders = Order.objects.order_by('id').order_by('-id')[:10:]
    order = Order.objects.all()

    sales_data = OrderItem.objects.values('order__created_at__date').annotate(
        total_sale=Sum('price')).order_by('-order__created_at__date')
    categories = [item['order__created_at__date'].strftime(
        '%d/%m') for item in sales_data]
    sales_values = [item['total_sale'] for item in sales_data]
    return_data = OrderItem.objects.filter(status__in=["Return", "Cancelled"]).values(
        'order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
    return_values = [item['total_returns'] for item in return_data]
    print(return_values)
    print(sales_values)
    try:
        total_sale = 0
        order = Order.objects.all()
        for i in order:
            i.total_price
            total_sale += i.total_price
    except:
        total_sale = 0

    try:
        total_earning = 0
        order_ear = Order.objects.filter(status='Delivered')
        for i in order_ear:
            total_earning += i.total_price
    except:
        total_earning = 0
    try:
        status_delivery = Order.objects.filter(status='Delivered').count()
        status_return = Order.objects.filter(status='Return').count()
        status_cancel = Order.objects.filter(status='Cancelled').count()
        total = status_delivery + status_return + status_cancel
        status_delivery = (status_delivery/100)*total
        status_cancel = (status_cancel/100)*total
        status_return = (status_return/100)*total
    except:
        status_delivery = 0
        status_cancel = 0
        status_return = 0

    print(status_cancel)
    print(total_sale)
    print(total_earning)
    print(status_return)
    print(status_return)
    print(sales_values)
    context = {
        'orders': orders,
        'total_sale': total_sale,
        'total_earning': total_earning,
        'total_sale': total_sale,
        'status_return': status_return,
        'status_cancel': status_cancel,
        'status_delivery': status_delivery,
        'sales_values': sales_values,
        'return_values': return_values,
        'categories': categories
    }
    return render(request, 'Admin-temp/dashboard.html', context)


# PRODUCT  MANAGEMENT
@never_cache
@login_required(login_url='signin')
def product_management(request):
    if request.user.is_superadmin:
        if request.method == "POST":
            key = request.POST['key']
            products = Product.objects.filter(Q(product_name__icontains=key) | Q(
                slug__startswith=key) | Q(category__category_name__startswith=key)).order_by('id')
        else:
            products = Product.objects.all().order_by('id')
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products': paged_products
        }
        return render(request, 'Admin-temp/product_list.html', context)
    else:
        return redirect('Home')


# ADD PRODUCT
@never_cache
@login_required(login_url='signin')  # type: ignore
def add_product(request):
    if request.user.is_superadmin:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('product_list')
            else:
                messages.error(request, 'Already Added product')
                return redirect('add_product')
        else:
            form = ProductForm()
            context = {
                'form': form
            }
            return render(request, 'Admin-temp/add_product.html', context)
    else:
        return redirect('Home')

# EDIT PRODUCT


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)
    if request.user.is_superadmin:
        if request.method == 'POST':
            try:
                form = ProductForm(
                    request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Product edited succefully')
                    return redirect('add_product')
                else:
                    messages.error(request, 'Invalid form')
                    return redirect('edit_product')

            except Exception as e:
                raise e

        context = {
            'product': product,
            'form': form
        }
        return render(request, 'Admin-temp/edit_product.html', context)
    else:
        return redirect('Home')

# DELETE PRODUCTS


@never_cache
@login_required(login_url='signin')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.error(request, 'Product deleted Successfully')
    return redirect('product_list')


# USER MANAGMENT
@never_cache
@login_required(login_url='signin')
def user_management(request):
    if request.user.is_superadmin:
        if request.method == "POST":
            key = request.POST['key']
            users = Account.objects.filter(Q(first_name__startswith=key) | Q(last_name__startswith=key) | Q(
                username__startswith=key) | Q(email__startswith=key), is_superadmin=False).order_by('id')
        else:
            users = Account.objects.filter(is_superadmin=False).order_by('id')

        paginator = Paginator(users, 10)
        page = request.GET.get('page')
        paged_users = paginator.get_page(page)
        context = {
            'users': paged_users
        }
        return render(request, 'Admin-temp/user_management.html', context)
    else:
        return redirect('Login')

# BLOCK USER


@never_cache
@login_required(login_url='Login')
def block_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_management')

# USER UNBLOCK


@never_cache
@login_required(login_url='Login')
def unblock_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_management')


@never_cache
@login_required(login_url='signin')
def user_view(request, user_id=None):
    # If user_id is not provided, get details of the currently logged-in user
    if user_id is None:
        user_id = request.user.id

    if request.user.is_superadmin:
        user = get_object_or_404(Account, id=user_id)
        context = {
            'user': user
        }
        return render(request, 'Admin-temp/user_view.html', context)
    else:
        return redirect('Login')


# CATOGERY MANAGEMENT
def category_management(request):
    if request.user.is_superadmin:
        categories = Category_list.objects.all().order_by('id')

        context = {
            'categories': categories
        }
        return render(request, 'Admin-temp/category_management.html', context)
    else:
        return redirect('Home')

# ADD CATEGORY


def add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST['category_name']
            category_description = request.POST['category_description']

            # Check if the category already exists
            if Category_list.objects.filter(category_name=category_name).exists():
                messages.error(
                    request, 'Category with this name already exists.')
            else:
                category = Category_list(
                    category_name=category_name,
                    category_description=category_description
                )
                category.save()
                messages.success(request, 'Category added successfully.')

            return redirect('category_management')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'Admin-temp/add_category.html')
# UPDATE CATEGORY


def edit_category(request, category_id):
    try:
        categories = Category_list.objects.get(id=category_id)

        if request.method == 'POST':
            category_name = request.POST['category_name']
            category_description = request.POST['category_description']
            categories.category_name = category_name
            categories.category_description = category_description

            categories.save()
            return redirect('category_management')

        context = {
            'category': categories,
        }
    except Exception as e:
        raise e

    return render(request, 'Admin-temp/edit_category.html', context)

# DELETE CATEGORY


def delete_category(request, category_id):
    categories = Category_list.objects.get(id=category_id)
    print(categories)
    categories.delete()
    return redirect('category_management')


# ORDER MANAGEMENT
def order_management(request):
    if request.user.is_superadmin:
        if request.method == 'POST':
            key = request.POST['key']
            order = Order.objects.filter(Q(tracking_no_startswith=key) | Q(
                useremailstartswith=key) | Q(first_name_startswith=key)).order_by('-id')
        else:
            order = Order.objects.all().order_by('-id')
        paginator = Paginator(order, 10)
        page = request.GET.get('page')
        paged_order = paginator.get_page(page)

        context = {
            'order': paged_order
        }
        return render(request, 'Admin-temp/order_management.html', context)
    else:
        return redirect('Home')

# VIEW MANAGEMENT ORDER


def manager_vieworder(request, tracking_no):
    if request.user.is_superadmin:
        order = Order.objects.filter(tracking_no=tracking_no).first()
        orderitems = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'orderitems': orderitems,
        }
        return render(request, 'Admin-temp/order_view.html', context)
    else:
        return redirect('Home')


# ACCEPT ORDER
def manager_accept_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Out For Shipping'
    order.save()
    return redirect('order_management')

# SHIP ORDER


def manager_ship_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Shipped'
    order.save()
    return redirect('order_management')

# DELIVERED ORDER


def manager_delivered_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Delivered'
    order.save()
    return redirect('order_management')

# CANCEL ORDER


def manager_cancel_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Cancelled'
    order.save()
    return redirect('order_management')


# MULTIPLE IMAGES MANAGEMENT
@never_cache
@login_required(login_url='signin')
def multiple_image_management(request):
    multipleimages = MultipleImages.objects.all().order_by('id')
    paginator = Paginator(multipleimages, 10)
    page = request.GET.get('page')
    multipleimages = paginator.get_page(page)

    context = {
        'multipleimages': multipleimages
    }
    return render(request, 'Admin-temp/multiple_image_management.html', context)


# ADD MULTIPLE IMAGES
@never_cache
@login_required(login_url='signin')
def add_multiple_images(request):  # type: ignore
    if request.method == 'POST':
        form = MultipleImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, '')
            return redirect('multiple_image_management')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form')
            return redirect('add_multiple_images')
    else:
        form = MultipleImagesForm()

    context = {
        'form': form
    }
    return render(request, 'Admin-temp/add_multiple_images.html', context)

# UPDATE MULTIPLE IMAGE


@never_cache
@login_required(login_url='signin')
def update_multiple_images(request, multi_id):
    multipleimages = MultipleImages.objects.get(id=multi_id)
    form = MultipleImagesForm(instance=multipleimages)
    if request.method == 'POST':
        form = MultipleImagesForm(
            request.POST, request.FILES, instance=multipleimages)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added Succefully')
            return redirect('multiple_image_management')
        else:
            messages.error(request, 'Invalid form')
            return redirect('update_multiple_images')
    context = {
        'form': form
    }
    return render(request, 'Admin-temp/update_multiple_images.html', context)


# DELETE MULTIPLEIMAGES
@never_cache
@login_required(login_url='signin')
def delete_multiple_images(request, multi_id):
    multipleimages = MultipleImages.objects.get(id=multi_id)
    multipleimages.delete()

    return redirect('multiple_image_management')


@login_required(login_url='signin')
def sales_report(request):
    try:
        start_date = None
        end_date = None
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                print('start date and end date', start_date, end_date)
                if start_date > end_date:
                    messages.error(request, 'Start date must be end date')
                    return redirect('adminside:dashboard')
                if end_date > date.today():
                    messages.error(request, 'End date cannot be in the future')
                    return redirect('adminside:dashboard')
                orders = Order.objects.filter(
                    created_at__date__range=(start_date, end_date))
                print('the order is the ', orders)
                recend_order = orders.order_by('created_at')
                total_sale = sum(order.total_price for order in orders)
                total_count = orders.count()

                sales_by_status = {
                    'Pending': orders.filter(od_status='Pending').count(),
                    'Processing': orders.filter(od_status='Processing').count(),
                    'Shipped': orders.filter(od_status='Shipped').count(),
                    'Delivered': orders.filter(od_status='Delivered').count(),
                    'Cancelled': orders.filter(od_status='Cancelled').count(),
                    'Return': orders.filter(od_status='Return').count()
                }

                sales_report = {
                    'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
                    'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
                    'total_sales': total_sale,
                    'total_orders': total_count,
                    'sales_by_status': sales_by_status,
                    'recent_orders': recend_order,
                }
                context = {
                    'sales_report': sales_report,
                }
                print('the total sale is the ', total_sale)
                return render(request, 'adminside/salesreport.html', context)

        recend = Order.objects.order_by('created_at')[:10]
        orders = Order.objects.all()
        total_sale = sum(order.total_price for order in orders)
        total_count = orders.count()

        sales_by_status = {
            'Pending': orders.filter(od_status='Pending').count(),
            'Processing': orders.filter(od_status='Processing').count(),
            'Shipped': orders.filter(od_status='Shipped').count(),
            'Delivered': orders.filter(od_status='Delivered').count(),
            'Cancelled': orders.filter(od_status='Cancelled').count(),
            'Return': orders.filter(od_status='Return').count()
        }

        sales_report = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
            'total_sales': total_sale,
            'total_orders': total_count,
            'sales_by_status': sales_by_status,
            'recent_orders': recend,
        }
        context = {
            'sales_report': sales_report,
        }
        print('the total sale is the ', total_sale)
        return render(request, 'Admin-temp/sales_report.html', context)
    except Exception as e:
        print(e)
        return render(request, 'Admin-temp/sales_report.html')


# Coupon
@login_required(login_url='signin')
def coupon(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon': coupon
    }
    return render(request, 'Admin-temp/coupon.html', context)


@login_required(login_url='signin')
def add_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_price = request.POST.get('min_price')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Validate coupon_code, discount, min_price, start_date, and end_date here
        if not coupon_code or not discount or not min_price or not start_date_str or not end_date_str:
            messages.error(request, 'All fields are required.')
        elif not discount.isdigit() or not min_price.isdigit():
            messages.error(
                request, 'Discount and minimum price should be numeric.')
        else:
            try:
                discount = int(discount)
                min_price = int(min_price)
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                if discount < 0 or min_price < 0:
                    messages.error(
                        request, 'Discount and minimum price should be non-negative.')
                elif start_date >= end_date:
                    messages.error(
                        request, 'End date must be after start date.')
                elif min_price <= discount:
                    messages.error(
                        request, 'Minimum price should be greater than the discount amount.')
                else:
                    new_coupon = Coupon(
                        coupon_code=coupon_code,
                        discount=discount,
                        min_price=min_price,
                        start_date=start_date,
                        end_date=end_date
                    )

                    new_coupon.save()
                    messages.success(request, 'Coupon added successfully.')
                    return redirect('coupon')
            except ValueError:
                messages.error(
                    request, 'Invalid date format. Please use YYYY-MM-DD.')

    return render(request, 'Admin-temp/add_coupon.html')


@login_required(login_url='signin')
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_price = request.POST.get('min_price')
        min_price = request.POST.get('min_price')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Add validation for coupon_code, discount, and min_price here
        if not coupon_code or not discount or not min_price:
            messages.error(request, 'All fields are required.')
        elif not discount.isdigit() or not min_price.isdigit():
            messages.error(
                request, 'Discount and minimum price should be numeric.')
        else:
            coupon.coupon_code = coupon_code
            coupon.discount = discount
            coupon.min_price = min_price
            coupon.save()
            messages.success(request, 'Coupon updated successfully.')
            return redirect('coupon')

    return render(request, 'Admin-temp/edit_coupon.html', {'i': coupon})


@login_required(login_url='signin')
def coupon_delete(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if not coupon.is_deleted:
        coupon.is_deleted = True
        coupon.save()
        messages.error(request, 'Deleted successfully')

    return redirect('coupon')


@login_required(login_url='signin')
def coupon_undelete(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if coupon.is_deleted:
        coupon.is_deleted = False
        coupon.save()
        messages.error(request, 'Undeleted successfully')

    return redirect('coupon')


# OFFER

@login_required(login_url='signin')
def offer(request):
    off = Offer.objects.all()
    context = {
        'off': off
    }
    return render(request, 'Admin-temp/offer.html', context)


@login_required(login_url='signin')
def add_offer(request):
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        discount_amount = request.POST.get('discount_amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Perform your custom validation here
        if not offer_name or not discount_amount or not start_date or not end_date:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                discount_amount = int(discount_amount)
                # Perform additional validation if needed
                if discount_amount < 0:
                    messages.error(
                        request, 'Discount amount must be a non-negative integer.')
                else:
                    new_offer = Offer(
                        offer_name=offer_name,
                        discount_amount=discount_amount,
                        start_date=start_date,
                        end_date=end_date,
                    )
                    new_offer.save()
                    messages.success(request, 'Offer added successfully!')
                    return redirect('offer')
            except ValueError:
                messages.error(
                    request, 'Discount amount must be a valid integer.')

    return render(request, 'Admin-temp/add_offer.html')


@login_required(login_url='signin')
def edit_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id)

    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        discount_amount = request.POST.get('discount_amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Update the offer data without any validation
        offer.offer_name = offer_name
        offer.discount_amount = discount_amount
        offer.start_date = start_date
        offer.end_date = end_date
        offer.save()
        messages.success(request, 'Offer updated successfully!')
        return redirect('offer')

    return render(request, 'Admin-temp/edit_offer.html', {'i': offer})


@login_required(login_url='signin')
def offer_delete(request, offer_id):

    offer = get_object_or_404(Offer, id=offer_id)
    # Assuming you have a field 'is_deleted' in your Offer model
    if not offer.is_deleted:
        offer.is_deleted = True
        offer.save()
        messages.error(request, 'Offer deleted successfully.')
    return redirect('offer')


@login_required(login_url='signin')
def offer_undelete(request, offer_id):

    offer = get_object_or_404(Offer, id=offer_id)

    if offer.is_deleted:
        offer.is_deleted = False
        offer.save()
        messages.success(request, 'Offer undeleted successfully.')
    return redirect('offer')


@login_required(login_url='Login')
def export_csv(request, start_date=None, end_date=None):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Expenses' + \
            str(datetime.now()) + '.csv'

        writer = csv.writer(response)
        # heading for csv
        writer.writerow(['user', 'total_price', 'payment_mode', 'tracking number',
                        'Order at', 'product_name', 'product_price', 'product_quantity'])
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = Order.objects.filter(
                created_at__date__range=(start_date_obj, end_date_obj))
        else:
            orders = Order.objects.all()

        for order in orders:
            order_item = OrderItem.objects.filter(
                order=order).select_related('product')
            grouped_order_items = groupby(order_item, key=lambda x: x.order_id)
            for order_id, items_group in grouped_order_items:
                item_list = list(items_group)
                for order_item in item_list:
                    writer.writerow([
                        order.user.username if order_item == item_list[0] else " ",
                        order.total_price if order_item == item_list[0] else " ",
                        order.payment_mode if order_item == item_list[0] else " ",
                        order.tracking_no if order_item == item_list[0] else " ",
                        order.created_at if order_item == item_list[0] else " ",
                        order_item.product.product_name,
                        order_item.product.product_price,
                        order_item.quantity
                    ])
        return response
    except Exception as e:
        print(e)
        return render(request, 'Admin-temp/sales_report.html')


@login_required(login_url='Login')
def pdf(request, start_date=None, end_date=None):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Expenses' + \
            str(datetime.now()) + '.pdf'

        w_pt = 8.5 * 40  # 8.5 inches width
        h_pt = 11 * 20   # 11 inches hieght

        pdf = FPDF(format=(w_pt, h_pt))
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # set the style
        pdf.set_font('Arial', 'B', 12)

        # Header Information
        pdf.cell(0, 10, 'Order Details Report', 0, 1, 'C')
        pdf.cell(0, 10, str(datetime.now()), 0, 1, 'C')

        data = [['user', 'Toatl price', 'Payement Mode', 'Tracking Number',
                 'Odered_at', 'Product Name', 'Product Price', 'Prduct Quantity']]
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = Order.objects.filter(created_at__date__range=(start_date_obj, end_date_obj)).prefetch_related(
                Prefetch('orderitem_set',
                         queryset=OrderItem.objects.select_related('product'))
            )
        else:
            orders = Order.objects.all().prefetch_related(
                Prefetch('orderitem_set',
                         queryset=OrderItem.objects.select_related('product'))
            )
        for order in orders:
            order_item = order.orderitem_set.all()
            for index, order_item in enumerate(order_item):
                data.append([
                    order.user.username if index == 0 else "",
                    order.total_price if index == 0 else "",
                    order.payment_mode if index == 0 else "",
                    order.tracking_no if index == 0 else "",
                    str(order.created_at.date()) if index == 0 else "",
                    order_item.product.product_name,
                    order_item.product.product_price,
                    order_item.quantity,
                ])
        # Create Table
        col_width = 40
        row_height = 10
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1)
            pdf.ln()
        response.write(pdf.output(dest='S').encode('latin1'))
        return response
    except Exception as e:
        print(e)
        return render(request, 'Admin-temp/sales_report.html')
