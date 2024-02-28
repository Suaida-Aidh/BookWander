from django.db import models
from store.models import Product
from Authentication.models import Account

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    cart_id    = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product   = models.ForeignKey(Product,on_delete=models.CASCADE)  
    cart      = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity  =  models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
       return self.product.price * self.quantity  

    def __unicode__(self):
        return self.product  


class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
                 

# class UserAddressBook(models.Model):
#     user=models.ForeignKey(Account, on_delete=models.CASCADE)
#     address=models.TextField()
#     status=models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural='AddressBook'



