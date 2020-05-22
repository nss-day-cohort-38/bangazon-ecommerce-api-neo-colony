from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .customer import Customer
from .paymenttype import PaymentType

class Order(models.models):
    
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE )
    payment_type_id = models.ForeignKey(PaymentType, on_delete = models.CASCADE )
    created_at = models.DateTimeField()
    
    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")        
        
    def __str__(self):
        return f"Customer ID: {self.customer_id}  Payment Type:{self.payment_type_id} Created At:{self.created_id}"
    
    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})