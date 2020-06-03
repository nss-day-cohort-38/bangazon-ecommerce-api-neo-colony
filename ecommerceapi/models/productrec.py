from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .customer import Customer
from .product import Product
from django.contrib.auth.models import User
# from .producttype import ProductType

class ProductRec(models.Model):
    
    sender = models.ForeignKey(Customer, related_name="sender", on_delete = models.CASCADE )
    reciever = models.ForeignKey(Customer, related_name="reciever", on_delete = models.CASCADE )
    product =  models.ForeignKey(Product, on_delete = models.CASCADE )   
    
    class Meta:
        verbose_name = ("ProductRec")
        verbose_name_plural = ("ProductRecs")        
        
    def __str__(self):
        return f"ProductRec Id: {self.id}"
    
    def get_absolute_url(self):
        return reverse("ProductRec_detail", kwargs={"pk": self.pk})    