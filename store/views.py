from django.shortcuts import render
from .models import Category_list, Product, Authors
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def shop(request):

    products = Product.objects.all().filter(is_available=True)
    products_ascending = Product.objects.all().filter(is_available=True).order_by('product_name')
    products_high_to_low = Product.objects.all().filter(is_available=True).order_by('price')

    # cart_items = CartItem.objects.all()
    Categories = Category_list.objects.all()
    authors = Authors.objects.all()

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)
    paginator2 = Paginator(products_ascending, per_page)
    paginator3 = Paginator(products_high_to_low, per_page)

    try:
        current_page = paginator.page(page_number)
        current_page2 = paginator2.page(page_number)
        current_page3 = paginator3.page(page_number)
    
    except PageNotAnInteger:
        # If the 'page' parameter is not an integer, display the first page
        current_page = paginator.page(1)
        current_page2 = paginator2.page(1)
        current_page3 = paginator3.page(1)

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        current_page2 = paginator2.page(paginator.num_pages)
        current_page3 = paginator3.page(paginator.num_pages)

    context = {
        "current_page3": current_page3,
        "current_page2": current_page2,
        "current_page": current_page,
        "categories": Categories,
        "authors": authors,
        "products": products,
        "products_old_books" : products[3:],
        "products_popular" : products[2:5],
        # "cart_items" : cart_items,
    }
    
    return render(request, 'User/shop.html', context)

