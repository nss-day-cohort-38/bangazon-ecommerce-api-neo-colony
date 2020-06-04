from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .customer import Customer
from .producttype import ProductType

class Product(models.Model):
    
    title = models.CharField(null = False, max_length = 50 )
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE )
    price = models.FloatField(null = False)
    description = models.CharField(null = False, max_length = 255 )
    quantity = models.IntegerField(null = False)
    location = models.CharField(null = False, max_length = 75 )
    image = models.ImageField(upload_to='ecommerceapi_images', null=True)
    created_at = models.DateTimeField(auto_now_add= True)
    product_type = models.ForeignKey(ProductType, related_name="products", null = False, on_delete = models.DO_NOTHING)
    sold_products = 0
    
    
    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")        
        
    def __str__(self):
        return f"Title: {self.title}"
    
    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})    