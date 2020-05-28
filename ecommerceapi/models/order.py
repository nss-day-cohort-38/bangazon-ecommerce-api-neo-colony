from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .customer import Customer
from .paymenttype import PaymentType



class Order(models.Model):
    
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE )
    payment_type = models.ForeignKey(PaymentType, on_delete = models.CASCADE )
    created_at = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")        
        
    def __str__(self):
        return f"Customer ID: {self.customer}  Payment Type:{self.payment_type} Created At:{self.created}"
    
    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})