from django.urls import path
from . import views

app_name='payment'
urlpatterns = [
    path('', views.index, name="index"),
    path('charge/', views.charge, name="charge"),
    path('success/', views.successMsg, name="success"),
]
