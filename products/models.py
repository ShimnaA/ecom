from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, default='')
    photo = models.URLField(max_length=900, default='https://via.placeholder.com/300x400?text=No+photo')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product-detail', args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse("orders:add-to-cart", args=[str(self.slug)])
        #return reverse("orders:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("orders:remove-from-cart", args=[str(self.slug)])

class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    comment = models.TextField(max_length=2000, default='')
    date_posted = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return self.user.username

