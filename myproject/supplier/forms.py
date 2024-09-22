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


class RequisitionForm(forms.Form):
    description = forms.CharField(label='Description', max_length=255, required=True)
    justification = forms.CharField(label='Justification', max_length=255, required=True)
    
    line_number = forms.IntegerField(label='Line Number', initial=1, required=True)
    line_type_code = forms.CharField(label='Line Type Code', max_length=50, initial="Goods", required=True)
    category_name = forms.CharField(label='Category Name', max_length=100, initial="Miscellaneous", required=True)
    item_description = forms.CharField(label='Item Description', max_length=255, required=True)
    quantity = forms.IntegerField(label='Quantity', required=True)
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2, required=True)
    currency_code = forms.CharField(label='Currency Code', max_length=10, initial="USD", required=True)
    uom = forms.CharField(label='Unit of Measure', max_length=10, initial="Ea", required=True)
    
    requester_id = forms.IntegerField(label='Requester ID', initial=300000047340498, required=True)
    destination_organization_id = forms.IntegerField(label='Destination Organization ID', required=True)
    deliver_to_location_id = forms.IntegerField(label='Deliver To Location ID', initial=300000047013160, required=True)
    requested_delivery_date = forms.DateField(label='Requested Delivery Date', widget=forms.TextInput(attrs={'type': 'date'}), required=True)