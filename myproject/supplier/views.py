from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .forms import SupplierForm

def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            supplier_name = form.cleaned_data['supplier_name']
            tax_organization_type = form.cleaned_data['tax_organization_type']
            supplier_type = form.cleaned_data['supplier_type']
            business_relationship = form.cleaned_data['business_relationship']
            address_name = form.cleaned_data['address_name']
            country = form.cleaned_data['country']
            address_line1 = form.cleaned_data['address_line1']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            county = form.cleaned_data['county']
            procurement_bu = form.cleaned_data['procurement_bu']
            contact_first_name = form.cleaned_data['contact_first_name']
            contact_last_name = form.cleaned_data['contact_last_name']
            contact_email = form.cleaned_data['contact_email']
            phone_country_code = form.cleaned_data['phone_country_code']
            phone_area_code = form.cleaned_data['phone_area_code']
            phone = form.cleaned_data['phone']

            # Construct the SOAP request payload
            soap_payload = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                              xmlns:typ="http://xmlns.oracle.com/apps/prc/poz/suppliers/supplierServiceV2/types/"
                              xmlns:sup="http://xmlns.oracle.com/apps/prc/poz/suppliers/supplierServiceV2/"
                              xmlns:sup1="http://xmlns.oracle.com/apps/flex/prc/poz/suppliers/supplierServiceV2/supplierSites/"
                              xmlns:sup2="http://xmlns.oracle.com/apps/flex/prc/poz/suppliers/supplierServiceV2/supplierAddress/"
                              xmlns:sup3="http://xmlns.oracle.com/apps/flex/prc/poz/suppliers/supplierServiceV2/supplier/"
                              xmlns:sup4="http://xmlns.oracle.com/apps/flex/prc/poz/suppliers/supplierServiceV2/supplierContact/">
                <soapenv:Header/>
                <soapenv:Body>
                    <typ:createSupplier>
                        <typ:supplierRow>
                            <sup:Supplier>{supplier_name}</sup:Supplier>
                            <sup:TaxOrganizationType>{tax_organization_type}</sup:TaxOrganizationType>
                            <sup:SupplierType>{supplier_type}</sup:SupplierType>
                            <sup:BusinessRelationship>{business_relationship}</sup:BusinessRelationship>

                            <sup:SupplierAddresses>
                                <sup:Operation>CREATE</sup:Operation>
                                <sup:AddressName>{address_name}</sup:AddressName>
                                <sup:Country>{country}</sup:Country>
                                <sup:AddressLine1>{address_line1}</sup:AddressLine1>
                                <sup:City>{city}</sup:City>
                                <sup:State>{state}</sup:State>
                                <sup:County>{county}</sup:County>
                                <sup:OrderingPurposeFlag>FALSE</sup:OrderingPurposeFlag>
                                <sup:RemitToPurposeFlag>FALSE</sup:RemitToPurposeFlag>
                                <sup:RFQOrBiddingPurposeFlag>TRUE</sup:RFQOrBiddingPurposeFlag>
                            </sup:SupplierAddresses>

                            <sup:SupplierSites>
                                <sup:Operation>CREATE</sup:Operation>
                                <sup:SiteName>{address_name}</sup:SiteName>
                                <sup:AddressName>{address_name}</sup:AddressName>
                                <sup:ProcurementBU>{procurement_bu}</sup:ProcurementBU>
                                <sup:PurchasingPurposeFlag>TRUE</sup:PurchasingPurposeFlag>
                                <sup:AlternateSiteName>Main Office Purchasing</sup:AlternateSiteName>
                                <sup:CommunicationMethod>EMAIL</sup:CommunicationMethod>
                                <sup:EmailAddress>{contact_email}</sup:EmailAddress>
                            </sup:SupplierSites>

                            <sup:SupplierContacts>
                                <sup:Operation>CREATE</sup:Operation>
                                <sup:FirstName>{contact_first_name}</sup:FirstName>
                                <sup:LastName>{contact_last_name}</sup:LastName>
                                <sup:AdministrativeContactFlag>TRUE</sup:AdministrativeContactFlag>
                                <sup:EmailAddress>{contact_email}</sup:EmailAddress>
                                <sup:PhoneCountryCode>{phone_country_code}</sup:PhoneCountryCode>
                                <sup:PhoneAreaCode>{phone_area_code}</sup:PhoneAreaCode>
                                <sup:Phone>{phone}</sup:Phone>

                                <sup:SupplierContactAddresses>
                                    <sup:Operation>CREATE</sup:Operation>
                                    <sup:AddressName>{address_name}</sup:AddressName>
                                </sup:SupplierContactAddresses>
                            </sup:SupplierContacts>
                        </typ:supplierRow>
                    </typ:createSupplier>
                </soapenv:Body>
            </soapenv:Envelope>
            """

            # Send the SOAP request
            wsdl_url = 'https://edrx-dev1.fa.us2.oraclecloud.com/fscmService/SupplierServiceV2?WSDL'
            headers = {'Content-Type': 'text/xml;charset=UTF-8'}
            response = requests.post(wsdl_url, data=soap_payload, headers=headers, auth=('CSP_COMMON_USER1', 'CSP@Aug_2024'))

            # Check the response and return a message
            if response.status_code == 200:
                return HttpResponse("Supplier created successfully!")
            else:
                return HttpResponse(f"Failed to create supplier. Status code: {response.status_code} | Response: {response.text}")
    else:
        form = SupplierForm()

    return render(request, 'create_supplier.html', {'form': form})
