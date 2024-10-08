from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .forms import SupplierForm, RequisitionForm

# Function to send email
def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully!")

# Function to create supplier
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
                                <sup:OrderingPurposeFlag>TRUE</sup:OrderingPurposeFlag>
                                <sup:RFQOrBiddingPurposeFlag>TRUE</sup:RFQOrBiddingPurposeFlag>
                            </sup:SupplierAddresses>

                            <sup:SupplierSites>
                                <sup:Operation>CREATE</sup:Operation>
                                <sup:SiteName>{address_name}</sup:SiteName>
                                <sup:AddressName>{address_name}</sup:AddressName>
                                <sup:ProcurementBU>{procurement_bu}</sup:ProcurementBU>
                                <sup:PurchasingPurposeFlag>TRUE</sup:PurchasingPurposeFlag>
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
            wsdl_url = 'https://exsp-dev28.ds-fa.oraclepdemos.com:443/fscmService/SupplierServiceV2?WSDL'
            headers = {'Content-Type': 'text/xml;charset=UTF-8'}
            response = requests.post(wsdl_url, data=soap_payload, headers=headers, auth=('Rahul.gautam', 'Account@53211'))

            # Check the response and handle accordingly
            if response.status_code == 200:
                # Send confirmation email to the supplier
                send_email(
                    sender_email="Gautam.work98@gmail.com",
                    receiver_email=contact_email,
                    subject="Welcome to Our Supplier Portal",
                    body=f"""
                    Dear {contact_first_name} {contact_last_name},

                    We are pleased to inform you that your supplier account has been created successfully.

                    Best regards,
                    Your Company
                    """,
                    smtp_server="smtp.gmail.com",
                    smtp_port=465,
                    smtp_username="Gautam.work98@gmail.com",
                    smtp_password="bhpb uzpm vkfv uzod"  # App-specific password
                )

                # Redirect to supplier details page
                supplier_data = {
                    'supplier_name': supplier_name,
                    'tax_organization_type': tax_organization_type,
                    'supplier_type': supplier_type,
                    'business_relationship': business_relationship,
                    'address_name': address_name,
                    'country': country,
                    'address_line1': address_line1,
                    'city': city,
                    'state': state,
                    'county': county,
                    'procurement_bu': procurement_bu,
                    'contact_first_name': contact_first_name,
                    'contact_last_name': contact_last_name,
                    'contact_email': contact_email,
                    'phone_country_code': phone_country_code,
                    'phone_area_code': phone_area_code,
                    'phone': phone
                }
                return redirect(reverse('supplier_details') + '?' + urlencode(supplier_data))
            else:
                return HttpResponse(f"Failed to create supplier. Status code: {response.status_code} | Response: {response.text}")
    else:
        form = SupplierForm()

    return render(request, 'create_supplier.html', {'form': form})

# Supplier details view
def supplier_details(request):
    supplier_data = {
        'supplier_name': request.GET.get('supplier_name'),
        'tax_organization_type': request.GET.get('tax_organization_type'),
        'supplier_type': request.GET.get('supplier_type'),
        'business_relationship': request.GET.get('business_relationship'),
        'address_name': request.GET.get('address_name'),
        'country': request.GET.get('country'),
        'address_line1': request.GET.get('address_line1'),
        'city': request.GET.get('city'),
        'state': request.GET.get('state'),
        'county': request.GET.get('county'),
        'procurement_bu': request.GET.get('procurement_bu'),
        'contact_first_name': request.GET.get('contact_first_name'),
        'contact_last_name': request.GET.get('contact_last_name'),
        'contact_email': request.GET.get('contact_email'),
        'phone_country_code': request.GET.get('phone_country_code'),
        'phone_area_code': request.GET.get('phone_area_code'),
        'phone': request.GET.get('phone')
    }
    return render(request, 'supplier_details.html', {'supplier_data': supplier_data})


def create_requisition(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            # Extract form data
            data = form.cleaned_data

            # Prepare the payload for the API request
            payload = {
                "RequisitioningBUId": 300000046987012,
                "PreparerId": 300000047340498,
                "ExternallyManagedFlag": False,
                "Description": data['description'],
                "Justification": data['justification'],
                "lines": [
                    {
                        "LineNumber": data['line_number'],
                        "LineTypeCode": data['line_type_code'],
                        "CategoryName": data['category_name'],
                        "ItemDescription": data['item_description'],
                        "Item": None,
                        "Quantity": data['quantity'],
                        "Price": data['price'],
                        "CurrencyCode": data['currency_code'],
                        "UOM": data['uom'],
                        "RequesterId": data['requester_id'],
                        "DestinationTypeCode": "EXPENSE",
                        "DestinationOrganizationId": data['destination_organization_id'],
                        "DeliverToCustomerLocationId": None,
                        "DeliverToLocationId": data['deliver_to_location_id'],
                        "RequestedDeliveryDate": str(data['requested_delivery_date']),
                        "distributions": [
                            {
                                "Quantity": data['quantity'],
                                "DistributionNumber": 1
                            }
                        ]
                    }
                ]
            }

            # API endpoint URL
            url = "https://exsp-dev28.ds-fa.oraclepdemos.com:443/fscmRestApi/resources/11.13.18.05/purchaseRequisitions"

            # Send the POST request to Oracle API
            response = requests.post(
                url,
                json=payload,
                auth=('username', 'password'),  # Replace with actual username and password
                headers={'Content-Type': 'application/json'}
            )

            # Handle the API response
            if response.status_code == 201:
                return HttpResponse("Requisition created successfully!")
            else:
                return HttpResponse(f"Failed to create requisition. Status code: {response.status_code}, Response: {response.text}")

    else:
        form = RequisitionForm()

    return render(request, 'create_requisition.html', {'form': form})