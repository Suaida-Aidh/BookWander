from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from store.models import Product
from django.core.paginator import Paginator
from django.db.models import Q
from .form import ProductForm,MultipleImagesForm
from store.models import MultipleImages
from django.contrib import messages
from Authentication.models import Account
from store.models import Category_list
from order.models import Order, OrderItem
from django.shortcuts import render, get_object_or_404




# Create your views here.

def dashboard(request):
    return render (request,'Admin-temp/dashboard.html')

#PRODUCT  MANAGEMENT
@never_cache
@login_required(login_url='signin')
def product_management(request):
  if request.user.is_superadmin: 
    if request.method == "POST":
      key = request.POST['key']
      products = Product.objects.filter(Q(product_name__icontains=key) | Q(slug__startswith=key) | Q(category__category_name__startswith=key)).order_by('id')
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
  

#ADD PRODUCT
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
       messages.error(request,'Invalid form')
       return redirect('add_product')     
    else:
      form = ProductForm()
      context = {
          'form': form
       }
      return render(request, 'Admin-temp/add_product.html', context)
  else:
    return redirect('Home') 
  
#EDIT PRODUCT
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)
    if request.user.is_superadmin:
      if request.method == 'POST':
          try:
              form = ProductForm(request.POST, request.FILES, instance=product)
              if form.is_valid():
                  form.save()
                  messages.success(request,'Product edited succefully')
                  return redirect('add_product')
              else:
                messages.error(request,'Invalid form') 
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
  messages.error(request,'Product deleted Successfully')
  return redirect('product_list')



#USER MANAGMENT 
@never_cache
@login_required(login_url='signin')
def user_management(request):
    if request.user.is_superadmin:
        if request.method == "POST":
            key = request.POST['key']
            users = Account.objects.filter( Q(first_name__startswith=key) | Q(last_name__startswith=key) | Q(username__startswith=key) | Q(email__startswith=key),is_superadmin=False).order_by('id')
        else:
            users = Account.objects.filter(is_superadmin=False).order_by('id')

        paginator = Paginator(users,10)
        page = request.GET.get('page')
        paged_users = paginator.get_page(page)
        context = {
        'users' : paged_users
        }
        return render(request, 'Admin-temp/user_management.html',context)
    else:
        return redirect('Login')    
    
# BLOCK USER
@never_cache
@login_required(login_url='Login')
def block_user(request,user_id):
    user = Account.objects.get(id =user_id)
    user.is_active = False
    user.save()
    return redirect ('user_management') 

# USER UNBLOCK
@never_cache
@login_required(login_url='Login')
def unblock_user(request,user_id):
    user = Account.objects.get(id =user_id)
    user.is_active = True
    user.save()
    return redirect ('user_management') 

from django.shortcuts import render

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


#CATOGERY MANAGEMENT
def category_management(request):
  if request.user.is_superadmin:
    categories = Category_list.objects.all().order_by('id')

    context = {
          'categories': categories
      }
    return render(request, 'Admin-temp/category_management.html', context)
  else:
    return redirect('Home')  
  
#ADD CATEGORY
def add_category(request):
  if request.user.is_superadmin:
    if request.method == 'POST':
        try:
            category_name = request.POST['category_name']
            category_description = request.POST['category_description']

            categories = Category_list(
                category_name=category_name,
                category_description=category_description
            )

            categories.save()
            return redirect('category_management')
        except Exception as e:
            raise e

    return render(request, 'Admin-temp/add_category.html')
  else:
    return redirect('Home')  

#UPDATE CATEGORY  
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

#DELETE CATEGORY
def delete_category(request, category_id):
    categories = Category_list.objects.get(id=category_id)
    print(categories)
    categories.delete()
    return redirect('category_management')



#ORDER MANAGEMENT
def order_management(request):
  if request.user.is_superadmin:
    if request.method == 'POST':
        key = request.POST['key']
        order = Order.objects.filter( Q(tracking_no_startswith=key) | Q(useremailstartswith=key) | Q(first_name_startswith=key)).order_by('-id')
    else:
        order = Order.objects.all().order_by('-id') 
    paginator = Paginator(order, 10)
    page = request.GET.get('page')
    paged_order = paginator.get_page(page)

    context = {
        'order': paged_order
        }
    return render(request, 'Admin-temp/order_management.html',context)
  else:
    return redirect('Home')  
  
#VIEW MANAGEMENT ORDER
def manager_vieworder(request,tracking_no):
  if request.user.is_superadmin:
    order = Order.objects.filter(tracking_no=tracking_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'Admin-temp/order_view.html',context)
  else:
    return redirect('Home') 
  

#ACCEPT ORDER
def manager_accept_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Out For Shipping'
    order.save()
    return redirect('order_management')  

#SHIP ORDER    
def manager_ship_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Shipped'
    order.save()
    return redirect('order_management')

#DELIVERED ORDER
def manager_delivered_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Delivered'
    order.save()
    return redirect('order_management')          

#CANCEL ORDER
def manager_cancel_order(request,tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Cancelled'
    order.save()
    return redirect('order_management')





#MULTIPLE IMAGES MANAGEMENT
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




#ADD MULTIPLE IMAGES
@never_cache
@login_required(login_url='signin')
def add_multiple_images(request):  # type: ignore
  if request.method == 'POST':
    form = MultipleImagesForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.error(request,'')
      return redirect('multiple_image_management')
    else:
      print(form.errors)
      messages.error(request,'Invalid form') 
      return redirect('add_multiple_images') 
  else:
    form = MultipleImagesForm()

  context = {
    'form': form
  }
  return render(request,'Admin-temp/add_multiple_images.html',context)

# UPDATE MULTIPLE IMAGE
@never_cache
@login_required(login_url='signin')
def update_multiple_images(request,multi_id):
  multipleimages = MultipleImages.objects.get(id=multi_id)
  form = MultipleImagesForm(instance = multipleimages)
  if request.method == 'POST':
    form = MultipleImagesForm(request.POST, request.FILES, instance = multipleimages)
    if form.is_valid():
      form.save()
      messages.success(request,'Added Succefully')
      return redirect('multiple_image_management')
    else:
      messages.error(request,'Invalid form') 
      return redirect('update_multiple_images')   
  context = {
    'form':form
  }
  return render(request, 'Admin-temp/update_multiple_images.html', context)


# DELETE MULTIPLEIMAGES
@never_cache
@login_required(login_url='signin')
def delete_multiple_images(request, multi_id):
  multipleimages = MultipleImages.objects.get(id = multi_id)
  multipleimages.delete()
  return redirect('multiple_image_management')
  






