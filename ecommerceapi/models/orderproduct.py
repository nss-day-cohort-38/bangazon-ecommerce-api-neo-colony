from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .product import Product
from .order import Order

class OrderProduct(models.Model):
    
    order_id= models.ForeignKey(Order, on_delete = models.CASCADE )
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE )
    
    class Meta:
        verbose_name = ("OrderProduct")
        verbose_name_plural = ("OrderProducts")        
        
    def __str__(self):
        return f"Order ID: {self.order_id} Product ID: {self.product_id}"
    
    def get_absolute_url(self):
        return reverse("OrderProduct_detail", kwargs={"pk": self.pk})