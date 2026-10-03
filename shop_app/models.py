from django.db import models
from base.models import BaseModel
# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
