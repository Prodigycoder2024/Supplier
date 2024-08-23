from django import forms

class SupplierForm(forms.Form):
    name = forms.CharField(label='Supplier Name', max_length=100)
    email = forms.EmailField(label='Email')
    contact_number = forms.CharField(label='Contact Number', max_length=15)
    address = forms.CharField(label='Address', widget=forms.Textarea)