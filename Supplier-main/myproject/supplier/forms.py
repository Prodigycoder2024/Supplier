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


from django import forms

class RequisitionForm(forms.Form):
    # Define your fields here
    supplier_name = forms.CharField(label='Supplier Name')
    tax_organization_type = forms.CharField(label='Tax Organization Type')
    supplier_type = forms.CharField(label='Supplier Type')
    business_relationship = forms.CharField(label='Business Relationship')
    address_name = forms.CharField(label='Address Name')
    country = forms.CharField(label='Country')
    address_line1 = forms.CharField(label='Address Line 1')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    county = forms.CharField(label='County')
    contact_first_name = forms.CharField(label='Contact First Name')
    contact_last_name = forms.CharField(label='Contact Last Name')
    contact_email = forms.EmailField(label='Contact Email')
    phone_country_code = forms.CharField(label='Phone Country Code')
    phone_area_code = forms.CharField(label='Phone Area Code')
    phone = forms.CharField(label='Phone')

    def __init__(self, *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control form-control-custom'
            })

