
from django.db import models
from Authentication.models import Account
from store.models import Product
from django.utils import timezone

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    first_name = models.CharField( max_length=50,blank=True)
    last_name = models.CharField( max_length=50,blank=True)
    phone = models.CharField(blank=True, max_length=50)
    email = models.EmailField( max_length=254,blank=True)
    address = models.CharField( max_length=50,blank=True)
    country = models.CharField( max_length=50,blank=True)
    state = models.CharField( max_length=50,blank=True)
    city = models.CharField( max_length=50,blank=True)
    pincode = models.CharField( max_length=50,blank=True)
    is_available = models.BooleanField(null=True,blank=True,default=True)
    image = models.ImageField( upload_to='userprofile',null=True,blank=True, height_field=None, width_field=None, max_length=None)

    def __str__(self) -> str:
        return f"{self.id}"


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150,null=False)
    email = models.EmailField(max_length=150,null=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address= models.TextField(max_length=150,null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=10,null=False)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id= models.CharField(max_length=500,null=True)
    tax_amount = models.FloatField(default=0.0) 
    multiple_address=models.ForeignKey(Address, on_delete=models.CASCADE,null=True)
    orderstatuses={
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return','Return'),
    
    }
    status = models.CharField(max_length=150,choices=orderstatuses,default='Pending')
    message=models.TextField(null=True)
    tracking_no =models.CharField(max_length=150,null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)  # type: ignore
    
   




class OrderItem(models.Model):


    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    price= models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=50, choices=[("Return", "Return"), ("Cancelled", "Cancelled"), ("Delivered", "Delivered")], default='default_value')



    def __str__(self):
        return'{} {}'.format(self.order.id, self.order.tracking_no)  # type: ignore

class Wallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return f"Wallet of {self.user.email}"

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=100)
    amount = models.FloatField()
    # created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} of ${self.amount} on {self.date_added}"

class Profile(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address= models.TextField(max_length=150,null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=10,null=False)
    created_at =models.DateTimeField(auto_now_add=True)
  # Manually define a default value

    def __str__(self):
        return self.user.email
    



# class Address(models.Model):
#     user = models.ForeignKey(Account, on_delete = models.CASCADE)
#     first_name = models.CharField(max_length=150, null=False)
#     last_name = models.CharField(max_length=150,null=False)
#     email = models.EmailField(max_length=150,null=False)
#     phone = models.CharField(max_length=15, null=True, blank=True)
#     city = models.CharField(max_length = 50)
#     country = models.CharField(max_length=150,null=False)
#     pincode=models.CharField(max_length=10,null=False)

#     # zipcode = models.IntegerField()
#     STATE_CHOICES = (
#     ('AL', 'Alabama'),
#     ('AK', 'Alaska'),
#     ('AZ', 'Arizona'),
#     ('KL', 'Kerala'),
# )
#     state = models.CharField(choices = STATE_CHOICES, max_length=50)







