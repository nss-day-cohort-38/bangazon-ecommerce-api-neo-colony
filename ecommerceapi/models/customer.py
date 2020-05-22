from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Customer(models.models):
    
    address = models.CharField(null = False, max_length = 50) 
    phone_number = models.CharField(null = False, max_length = 20)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")        
        
    def __str__(self):
        return f"User ID: {self.user_id}"
    
    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})
        