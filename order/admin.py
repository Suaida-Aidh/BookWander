from django.contrib import admin
from .models import Order,OrderItem,Wallet,Transaction,Profile,Address

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Profile)



@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    model = Address
    list_display = ['id', 'user', 'city', 'country', 'pincode', 'state']