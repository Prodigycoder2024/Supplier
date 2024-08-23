# supplier/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_form, name='supplier_form'),
]
