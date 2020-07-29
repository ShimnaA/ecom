from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from .models import Order, OrderItem
from django.contrib import messages
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #Check whether the order item is in the order
        order_item_qs = order.orderitem_set.filter(product__slug=slug)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated to your cart")
        else:
            order.orderitem_set.create(product=product)
            order.save()
            messages.info(request, "This item was added to your cart")
    else:
        order = Order.objects.create(user=request.user)
        order.orderitem_set.create(product=product)
        order.save()
        messages.info(request, "This item was added to your cart")
    return redirect("products:product-detail", pk=product.id)

@login_required
def remove_from_cart(request, slug):
    print("hello")
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        #Check whether the order item is in the order
        order_item_qs = order.orderitem_set.filter(product__slug=slug)
        if order_item_qs.exists():
            order_item_qs.delete()
            messages.info(request, "This item was removed from your cart")
            return redirect("products:product-detail", pk=product.id)
        else:
            messages.info(request, "This item was not in your cart")

            return redirect("products:product-detail", pk=product.id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products:product-detail", pk=product.id)


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            order_items = order.orderitem_set.all()
            context = {
                'order_items': order_items,
                'order_total_price': order.get_total_order_price,
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")





