from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [

    path('register/', views.register, name='register'),
]
