from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from store.models import Product
from django.core.paginator import Paginator
from django.db.models import Q
from .form import ProductForm
from django.contrib import messages
from Authentication.models import Account
from store.models import Category_list
from order.models import Order



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
                description=category_description
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
            categories.description = category_description

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





