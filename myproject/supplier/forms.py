# supplier/forms.py

from django import forms

class SupplierForm(forms.Form):
    supplier = forms.CharField(label='Supplier Name', max_length=100)
    tax_organization_type = forms.CharField(label='Tax Organization Type', max_length=100)
    supplier_type = forms.CharField(label='Supplier Type', max_length=100)
    business_relationship = forms.CharField(label='Business Relationship', max_length=100)
    duns_number = forms.CharField(label='DUNS Number', max_length=100)
    one_time_supplier_flag = forms.BooleanField(label='One-Time Supplier', required=False)
    taxpayer_country = forms.CharField(label='Taxpayer Country', max_length=100)
    taxpayer_id = forms.CharField(label='Taxpayer ID', max_length=100)
    