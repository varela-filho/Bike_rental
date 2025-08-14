from django.urls import path
from .views import index, prever

urlpatterns = [
    path('', index, name='index'),
    path('prever', prever, name='prever'),
]