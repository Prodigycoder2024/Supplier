# supplier/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # path('', views.supplier_form, name='supplier_form'),
    path('', create_supplier, name='create_supplier'),
     path('supplier-details/', supplier_details, name='supplier_details'),
]