
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from autoslug import AutoSlugField  
# from django.contrib.auth.models import User
# Create your models here.

class Category_list(models.Model):
    category_name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True, blank= True)
    category_description = models.TextField()
    is_available = models.BooleanField(default=False)
    # offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    


class Authors(models.Model):
    author_name = models.CharField(max_length=255)
    author_nation = models.CharField(max_length=255, null=True, blank=True)
    author_quotes = models.TextField(null=True, blank=True)
    author_description = models.TextField()
    author_image = models.ImageField(upload_to="phottos/authors", blank= True)
    author_birth_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'
    
    def __str__(self) -> str:
        return self.author_name



class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(max_length=200, unique=True, populate_from='product_name')  # Specify the source field
    product_description = models.TextField(max_length=300, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    images = models.ImageField( upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category_list, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def is_outofstock(self):
        return self.stock <= 0

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    # def get_offer_price(self):
    #     return int((self.price) - (self.price * self.offer.off_percent / 100))
    
    # def get_offer_price_by_category(self):
    #     return int((self.price) - (self.price * self.category.offer.off_percent / 100))

 
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to = 'product')


#multiple images
class MultipleImages(models.Model):
    image = models.ImageField(upload_to='media/product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)














    
