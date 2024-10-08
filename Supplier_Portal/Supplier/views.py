from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import requests
from .forms import *
from django.urls import reverse
from urllib.parse import urlencode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import JsonResponse
from django.views import View
from django.utils.dateparse import parse_datetime
from .models import *
from requests.auth import HTTPBasicAuth
from django.db.models import Q


def fetch_and_save_suppliers(request):
    # Base URL of the API
    base_url = "https://elbq-dev2.fa.us2.oraclecloud.com/fscmRestApi/resources/11.13.18.05/suppliers"
    username = 'mfg_portal'
    password = 'Oracle@123'

    # Get search parameter (SupplierNumber) from the request
    query = request.GET.get('q')
    
    # Add query parameter if present
    if query:
        url = f"{base_url}?q=SupplierNumber={query}"
    else:
        url = f"{base_url}?limit=1000"  # Default to getting all suppliers

    # Send GET request to the API
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        data = response.json()
        suppliers = data.get('items', [])  # Assuming the supplier list is under 'items' key

        # Loop through the supplier data and save to the database
        for supplier_data in suppliers:
            Supplier.objects.update_or_create(
                supplier_id=supplier_data['SupplierId'],
                defaults={
                    'supplier_party_id': supplier_data.get('SupplierPartyId', None),
                    'supplier_name': supplier_data.get('Supplier', ''),
                    'supplier_number': supplier_data.get('SupplierNumber', ''),
                    'alternate_name': supplier_data.get('AlternateName', None),
                    'tax_organization_type_code': supplier_data.get('TaxOrganizationTypeCode', ''),
                    'tax_organization_type': supplier_data.get('TaxOrganizationType', ''),
                    'supplier_type_code': supplier_data.get('SupplierTypeCode', ''),
                    'supplier_type': supplier_data.get('SupplierType', ''),
                    'inactive_date': supplier_data.get('InactiveDate', None),
                    'status': supplier_data.get('Status', ''),
                    'business_relationship_code': supplier_data.get('BusinessRelationshipCode', ''),
                    'business_relationship': supplier_data.get('BusinessRelationship', ''),
                    'parent_supplier_id': supplier_data.get('ParentSupplierId', None),
                    'parent_supplier': supplier_data.get('ParentSupplier', ''),
                    'parent_supplier_number': supplier_data.get('ParentSupplierNumber', ''),
                    'creation_date': supplier_data.get('CreationDate', None),
                    'created_by': supplier_data.get('CreatedBy', ''),
                    'last_update_date': supplier_data.get('LastUpdateDate', None),
                    'last_updated_by': supplier_data.get('LastUpdatedBy', ''),
                }
            )

        # Retrieve all suppliers from the database after saving
        suppliers = Supplier.objects.all().order_by('-creation_date')

        # Render suppliers on the frontend
        return render(request, 'suppliers.html', {'suppliers': suppliers})

    else:
        # In case of an error, return an empty table or error message
        return render(request, 'suppliers.html', {'suppliers': [], 'error': 'Failed to fetch data from API'})


# Function to display suppliers and allow searching by SupplierNumber from the API
def display_suppliers(request):
    query = request.GET.get('q')  # Get the search term from the URL query parameter

    if query:
        # Search by supplier name or supplier number using case-insensitive matching
        suppliers = Supplier.objects.filter(
            supplier_name__icontains=query
        ) | Supplier.objects.filter(
            supplier_number__icontains=query
        )
    else:
        # If no search term, show all suppliers
        suppliers = Supplier.objects.all()

    # Render the suppliers list and pass the search query to the template
    return render(request, 'suppliers.html', {'suppliers': suppliers, 'query': query})




def fetch_supplier_details(request, supplier_id):
    # Get supplier object
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    
    # API URLs for addresses and contacts
    addresses_url = f"https://elbq-dev2.fa.us2.oraclecloud.com/fscmRestApi/resources/11.13.18.05/suppliers/{supplier_id}/child/addresses"
    contacts_url = f"https://elbq-dev2.fa.us2.oraclecloud.com/fscmRestApi/resources/11.13.18.05/suppliers/{supplier_id}/child/contacts"
    
    username = 'mfg_portal'
    password = 'Oracle@123'

    # Fetch supplier addresses
    addresses_response = requests.get(addresses_url, auth=HTTPBasicAuth(username, password))
    addresses = addresses_response.json().get('items', []) if addresses_response.status_code == 200 else []

    # Fetch supplier contacts
    contacts_response = requests.get(contacts_url, auth=HTTPBasicAuth(username, password))
    contacts = contacts_response.json().get('items', []) if contacts_response.status_code == 200 else []

    # Render both addresses and contacts in the new template
    return render(request, 'each_supplier.html', {
        'supplier': supplier, 
        'addresses': addresses,
        'contacts': contacts
    })





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

            # Check the response and redirect to details page if successful
            if response.status_code == 200:
                # Send email to the supplier
                send_email(
                    sender_email="Gautam.work98@gmail.com",
                    receiver_email=contact_email,
                    subject="Welcome to Our Supplier Portal",
                    body=f"""
                    Dear {contact_first_name} {contact_last_name},

                    We are pleased to inform you that your supplier account has been created successfully.

                    Please do not hesitate to reach out if you have any questions.

                    Best regards,
                    Your Company
                    """,
                    smtp_server="smtp.gmail.com",
                    smtp_port=465,
                    smtp_username="Gautam.work98@gmail.com",
                    smtp_password="bhpb uzpm vkfv uzod"  # Replace with your actual app password
                )

                # Pass the necessary data for displaying supplier details
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

def supplier_details(request):
    # Extract supplier data from the request
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

    # Render the supplier details page with the supplier_data context
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