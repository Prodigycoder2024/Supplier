from django.shortcuts import render
from .forms import SupplierForm

def supplier_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact_number = form.cleaned_data['contact_number']
            address = form.cleaned_data['address']
            # You can now save this data to the database or process it as needed
    else:
        form = SupplierForm()
    return render(request, 'sup.html', {'form': form})
