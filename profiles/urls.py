from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profile, name='profiles'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<order_number>/', views.order_detail, name='order_detail'),
]
