from django.shortcuts import render
from .models import Product, Category, Review
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib import messages


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

#class ProductDetailView(DetailView):
#    model = Product
#    template_name = 'product_detail.html'
#
#    def get_context_data(self, **kwargs):
#        context = super(ProductDetailView, self).get_context_data(**kwargs)
#        context['categories'] = Category.objects.all()
#        return context

def productdetail(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(id=pk)
    review_qs = product.review_set.all()
    context = {
        'product': product,
        'categories': categories,
        'reviews': review_qs
    }
    return render(request, 'Product_detail.html', context)


def review(request, product_id):
    if request.method == 'POST':
        data = {
            'user': request.user,
            'rating': int(request.POST.get('rating')),
            'comment': request.POST.get('notes')
        }
        try:

            response = Review.objects.create(
                user=request.user,
                rating=data.get('rating'),
                comment=data.get('comment'),
                product=Product.objects.get(id=product_id)
            )
            print("added review")
            messages.success(request, "New Review added")
        except Exception as e:
            print(e)
            messages.warning(
                request, 'Got an error when trying to add a new Review')
    return redirect('/')



