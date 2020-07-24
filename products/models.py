from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse
#from django.contrib.auth import get_user_model

#User = get_user_model()
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, default='')
    photo = models.URLField(max_length=900, default='https://via.placeholder.com/300x400?text=No+photo')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product-detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

