from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .product import Product
from .order import Order
from collections import Counter


class OrderProduct(models.Model):
    
    order= models.ForeignKey(Order, on_delete = models.CASCADE )
    product = models.ForeignKey(Product, on_delete = models.CASCADE )
    ratings = Counter(ratings.values_list("rating", flat=True))
    
    class Meta:
        verbose_name = ("OrderProduct")
        verbose_name_plural = ("OrderProducts")        
        
    def __str__(self):
        return f"Order ID: {self.order} Product ID: {self.product}"
    
    def get_absolute_url(self):
        return reverse("OrderProduct_detail", kwargs={"pk": self.pk})