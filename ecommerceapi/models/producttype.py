from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class ProductType(models.Model):
    
    name = models.CharField(null = False, max_length = 55)
    
    class Meta:
        verbose_name = ("ProductType")
        verbose_name_plural = ("ProductTypes")        
        
    def __str__(self):
        return f"Name: {self.name}"
    
    def get_absolute_url(self):
        return reverse("ProductType_detail", kwargs={"pk": self.pk})