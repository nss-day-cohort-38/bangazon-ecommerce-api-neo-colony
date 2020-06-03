from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .customer import Customer
from .product import Product

class ProductLike(models.Model):
    
    like = models.BooleanField(null = True)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    
    class Meta:
        verbose_name = ("ProductLike")
        verbose_name_plural = ("ProductLikes")
        
    def __str__(self):
        return f"ProductLike ID: {self.id} "
    
    def get_absolute_url(self):
        return reverse("productlike_detail", kwargs={"pk": self.pk})
    
    