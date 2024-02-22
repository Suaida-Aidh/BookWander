
from django.db import models
from Authentication.models import Account
from store.models import Product

# Create your models here.


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
    orderstatuses={
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
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

    def __str__(self):
        return self.user.email
    



