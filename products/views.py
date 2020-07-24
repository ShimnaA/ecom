from django.shortcuts import render
from .models import Product, Category
from django.views.generic import DetailView


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(category__id=categories[0].id)
    context = {
        'products': products,
        'categories': categories,

    }
    return render(request, 'Homepage.html', context)

def product_list_category(request, category_id):
    categories = Category.objects.all()
    products = Product.objects.filter(category__id=category_id)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'Homepage.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context




