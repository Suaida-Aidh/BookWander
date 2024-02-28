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
from store.models import Category_list,Authors
from order.models import Order, OrderItem
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from datetime import datetime
from datetime import date
from django.core.exceptions import ValidationError
import csv
from django.http import HttpResponse
from fpdf import FPDF
from django.db.models import Prefetch
from itertools import groupby
from .context_processor import revenue_calculator
from django.db.models import Count
from django.utils import timezone

# Create your views here.
@login_required(login_url='Login')
def dashboard(request):
    orders = Order.objects.order_by('-id')[:10]
    sales_data = OrderItem.objects.values('order__created_at__date').annotate(
    total_sale=Sum('price')).order_by('-order__created_at__date')
    categories = [item['order__created_at__date'].strftime('%d/%m') for item in sales_data]
    sales_values = [item['total_sale'] for item in sales_data]

    return_data = OrderItem.objects.filter(status__in=["Return", "Cancelled"]).values(
        'order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
    return_values = [item['total_returns'] for item in return_data]

    total_sale = sum(order.total_price for order in Order.objects.all())
    orders_by_date = Order.objects.values('created_at__date').annotate(order_count=Count('id')).order_by('created_at__date')

    total_earning = sum(order.total_price for order in Order.objects.filter(status='Delivered'))

    status_delivery = Order.objects.filter(status='Delivered').count()
    status_return = Order.objects.filter(status='Return').count()
    status_cancel = Order.objects.filter(status='Cancelled').count()
    total = status_delivery + status_return + status_cancel
    status_delivery_percentage = (status_delivery / total) * 100
    status_return_percentage = (status_return / total) * 100

    dates = [item['created_at__date'].strftime('%Y-%m-%d') for item in orders_by_date]
    order_counts = [item['order_count'] for item in orders_by_date]


    # Call the revenue_calculator function
    revenue_context = revenue_calculator(request)
    revenue = revenue_context.get('revenue', 0)

    context = {
        'orders': orders,
        'total_sale': total_sale,
        'total_earning': total_earning,
        'status_return': status_return_percentage,
        'status_cancel': status_cancel,
        'status_delivery': status_delivery_percentage,
        'sales_values': sales_values,
        'return_values': return_values,
        'categories': categories,
        'revenue': revenue,
        'dates': dates,
        'order_counts': order_counts
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
    # try:
        start_date = None
        end_date = None
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                if start_date > end_date:
                    messages.error(request, 'Start date must be before end date')
                    return redirect('admin_dashboard')
                if end_date > timezone.localdate():
                    messages.error(request, 'End date cannot be in the future')
                    return redirect('admin_dashboard')
                orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
        else:
            orders = Order.objects.all()

        total_sale = sum(order.total_price for order in orders)

        total_count = orders.count()

        sales_by_status = {
            'Pending': orders.filter(status='Pending').count(),
            'Processing': orders.filter(status='Processing').count(),
            'Shipped': orders.filter(status='Shipped').count(),
            'Delivered': orders.filter(status='Delivered').count(),
            'Cancelled': orders.filter(status='Cancelled').count(),
            'Return': orders.filter(status='Return').count()
        }
        print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        print(sales_by_status)
        recent_orders = Order.objects.filter(created_at__range=(start_date, end_date))[:10]

        sales_report = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
            'total_sale': total_sale,
            'total_orders': total_count,
            'sales_by_status': sales_by_status,
            'recent_orders': recent_orders,
        }
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        print(sales_report)
        context = {
            'sales_report': sales_report,
        }
        print("ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
        print(context)
        return render(request, 'Admin-temp/sales_report.html', context)
    
    # except Exception as e:
    #     print(e)
    #     print("errrrrrrrrrrrrrrrrrrrrr")
    #     return render(request, 'Admin-temp/sales_report.html')





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





# AUTHOR MANAGEMENT______________________________________
    
def author_management(request):
    if request.user.is_superadmin:
        authors = Authors.objects.all().order_by('id')

        context = {
            'authors': authors
        }
        return render(request, 'Admin-temp/author_management.html', context)
    else:
        return redirect('Home')

# ADD CATEGORY


def add_author(request):
    if request.method == 'POST':
        try:
            author_name = request.POST['author_name']
            author_description = request.POST['author_description']

            # Check if the category already exists
            if Authors.objects.filter(author_name=author_name).exists():
                messages.error(
                    request, 'Author  name already exists.')
            else:
                authors = Authors(
                    author_name=author_name,
                    author_description=author_description
                )
                authors.save()
                messages.success(request, 'Author name  added successfully.')

            return redirect('author_management')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'Admin-temp/add_author.html')
# UPDATE CATEGORY


def edit_author(request, authors_id):
    try:
        authors = Authors.objects.get(id=authors_id)

        if request.method == 'POST':
            author_name = request.POST['author_name']
            author_description = request.POST['author_description']
            authors.author_name = author_name
            authors.author_description = author_description

            authors.save()
            return redirect('author_management')

        context = {
            'authors': authors,
        }
    except Exception as e:
        raise e

    return render(request, 'Admin-temp/edit_author.html', context)

# DELETE CATEGORY


def delete_author(request, authors_id):
    authors = Authors.objects.get(id=authors_id)
    print(authors)
    authors.delete()
    return redirect('author_management')

