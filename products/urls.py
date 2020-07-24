from django.urls import path, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('category/<str:category_id>', views.product_list_category, name='prod-category'),
    re_path(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product-detail'),

]
