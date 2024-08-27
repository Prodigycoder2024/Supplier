# # supplier/forms.py

# from django import forms

# class SupplierForm(forms.Form):
#     supplier = forms.CharField(label='Supplier Name', max_length=100)
#     tax_organization_type = forms.CharField(label='Tax Organization Type', max_length=100)
#     supplier_type = forms.CharField(label='Supplier Type', max_length=100)
#     business_relationship = forms.CharField(label='Business Relationship', max_length=100)
#     duns_number = forms.CharField(label='DUNS Number', max_length=100)
#     one_time_supplier_flag = forms.BooleanField(label='One-Time Supplier', required=False)
#     taxpayer_country = forms.CharField(label='Taxpayer Country', max_length=100)
#     taxpayer_id = forms.CharField(label='Taxpayer ID', max_length=100)
#     pass

# class AddressForm(forms.Form):
#     supplier_id = forms.ChoiceField(label="Supplier ID", choices=[])
#     address_name = forms.CharField(label="Address Name", max_length=100)
#     country = forms.CharField(label="Country", max_length=100)
#     address_line1 = forms.CharField(label="Address Line 1", max_length=255)
#     city = forms.CharField(label="City", max_length=100)
#     state = forms.CharField(label="State", max_length=100)
#     postal_code = forms.CharField(label="Postal Code", max_length=20)
#     ordering_flag = forms.BooleanField(label="Ordering Flag", required=False)
#     remit_to_flag = forms.BooleanField(label="Remit To Flag", required=False)
#     rfq_bidding_flag = forms.BooleanField(label="RFQ/Bidding Flag", required=False)
    
#     def __init__(self, *args, **kwargs):
#         suppliers = kwargs.pop('suppliers', [])
#         super(AddressForm, self).__init__(*args, **kwargs)
#         self.fields['supplier_id'].choices = [(supplier['SupplierId'], supplier['Supplier']) for supplier in suppliers]




from django import forms

class SupplierForm(forms.Form):
    supplier_name = forms.CharField(max_length=255, label='Supplier Name')
    tax_organization_type = forms.CharField(max_length=255, label='Tax Organization Type')
    supplier_type = forms.CharField(max_length=255, label='Supplier Type')
    business_relationship = forms.CharField(max_length=255, label='Business Relationship')
    
    address_name = forms.CharField(max_length=255, label='Address Name')
    country = forms.CharField(max_length=100, label='Country')
    address_line1 = forms.CharField(max_length=255, label='Address Line 1')
    city = forms.CharField(max_length=100, label='City')
    state = forms.CharField(max_length=100, label='State')
    county = forms.CharField(max_length=100, label='County')
    
    procurement_bu = forms.CharField(max_length=255, label='Procurement BU')
    
    contact_first_name = forms.CharField(max_length=100, label='Contact First Name')
    contact_last_name = forms.CharField(max_length=100, label='Contact Last Name')
    contact_email = forms.EmailField(label='Contact Email')
    phone_country_code = forms.CharField(max_length=10, label='Phone Country Code')
    phone_area_code = forms.CharField(max_length=10, label='Phone Area Code')
    phone = forms.CharField(max_length=20, label='Phone')
