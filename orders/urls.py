from django.urls import path, re_path
from .views import add_to_cart, remove_from_cart, OrderSummaryView, CheckoutView, PaymentView

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
]

