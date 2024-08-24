# supplier/views.py

import requests
from django.shortcuts import render
from .forms import SupplierForm

def supplier_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Prepare the payload
            payload = {
                "Supplier": form.cleaned_data['supplier'],
                "TaxOrganizationType": form.cleaned_data['tax_organization_type'],
                "SupplierType": form.cleaned_data['supplier_type'],
                "BusinessRelationship": form.cleaned_data['business_relationship'],
                "DUNSNumber": form.cleaned_data['duns_number'],
                "OneTimeSupplierFlag": form.cleaned_data['one_time_supplier_flag'],
                "TaxpayerCountry": form.cleaned_data['taxpayer_country'],
                "TaxpayerId": form.cleaned_data['taxpayer_id']
            }

            # Send the request to Oracle Cloud REST API
            response = requests.post(
                "https://edrx-dev1.fa.us2.oraclecloud.com/fscmRestApi/resources/11.13.18.05/suppliers",
                json=payload,
                auth=('CSP_COMMON_USER1', 'CSP@Aug_2024')
            )

            if response.status_code == 201:  # Created
                return render(request, 'success.html', {'supplier_name': form.cleaned_data['supplier']})
            else:
                return render(request, 'error.html', {'error_message': response.text})

    else:
        form = SupplierForm()

    return render(request, 'sup.html', {'form': form})
