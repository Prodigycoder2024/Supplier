# supplier/urls.py

from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # path('', views.supplier_form, name='supplier_form'),
    path('', create_supplier, name='create_supplier'),
    path('supplier-details/', supplier_details, name='supplier_details'),
    path('create-requisition/', views.create_requisition, name='create_requisition'),
    path('fetch-suppliers/', views.fetch_and_save_suppliers, name='fetch_and_save_suppliers'),
    # path('suppliers/', views.display_suppliers, name='display_suppliers'),
]