from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from .models import Order, CheckoutAddress, Payment
from django.contrib import messages
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
import stripe
from django.conf import settings
import json


def read_credentials():
    secrets = "secrets.json"
    with open(secrets) as f:
        keys = json.loads(f.read())
        return keys

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


class OrderSummaryView(LoginRequiredMixin, View):
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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        order_items = order.orderitem_set.all()
        context = {
            'form': form,
            'order_items': order_items,
            'order_total_price': order.get_total_order_price,
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            if form.is_valid():
                print("form is valid")
                print(form.cleaned_data)

                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                print(f"payment option {payment_option}")
                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                if payment_option == 'S':
                    return redirect("orders:payment", payment_option='stripe')
                elif payment_option == 'P':
                    return redirect("orders:payment", payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid option selected")
                    return redirect("orders:checkout")

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("orders:order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        order_items = order.orderitem_set.all()
        context = {
            'order_items': order_items,
            'order_total_price': order.get_total_order_price,
        }
        return render(self.request, "payment.html", context)

    def post(self, *args, **kwargs):
        #keys = read_credentials()
        #stripe.api_key = keys["STRIPE_SECRET_KEY"]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(stripe.api_key)
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        amount = int(order.get_total_order_price() * 100)
        token = self.request.POST['stripeToken']
        print(token)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # Create Payment
            print("create payment")
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_order_price()
            payment.save()

            # Assign payment to the order
            order.is_ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your Order was successful")
            #redirect to profile page or order success page
            return redirect("/")

        except stripe.error.CardError as e:
            messages.error(self.request, e.error.message)
            return redirect("/")

        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Too many requests made to the API")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid parameters were supplied to Stripe's API")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Authentication with Stripe's API failed")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network communication with Stripe failed")
            return redirect("/")
        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong, you were not charged, please try again")
            return redirect("/")
        except Exception as e:
            messages.error(self.request, "Error Occured")
            return redirect("/")










