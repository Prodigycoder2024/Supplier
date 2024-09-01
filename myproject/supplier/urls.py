# supplier/urls.py

from django.urls import path
from .views import create_supplier

urlpatterns = [
    # path('', views.supplier_form, name='supplier_form'),
    path('', create_supplier, name='create_supplier'),
    # path('update-address/', views.update_address, name='update_address'),
]