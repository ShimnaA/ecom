from django.contrib import admin
from .models import Order, OrderItem, CheckoutAddress, Payment

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
admin.site.register(Payment)
