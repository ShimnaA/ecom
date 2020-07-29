from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    def get_total_item_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_order_price(self):
        total = 0
        for orderitem in self.orderitem_set.all():
            total += orderitem.get_total_item_price()
        return total
