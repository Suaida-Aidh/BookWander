from order.models import Order,OrderItem
from django.shortcuts import render


def revenue_calculator(request):
    revenue = 10
    tax = 0
    total_revenue = 0
    try:
        orders = Order.objects.all()
        for order in orders:
            # Assuming tax is calculated as 10% of the total price
            tax += order.total_price * 0.1  # Adjust this calculation based on your tax rules
         
        order_items = OrderItem.objects.filter(order__status='Delivered')  # Filter only delivered items
        for item in order_items:
            revenue += item.price * item.quantity
     
        total_revenue = revenue + tax
        return render(request, 'Admin-temp/dashboard.html', {'revenue': total_revenue})
 
    except OrderItem.DoesNotExist:
        pass