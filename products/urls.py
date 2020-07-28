from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('category/<str:category_id>', views.product_list_category, name='prod-category'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

]
