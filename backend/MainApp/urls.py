"""
URL configuration for InfinitumAdmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#URL patters to route client requests to different view functions
from django.contrib import admin
from django.urls import path, re_path
from .views import api_upload_contract_worddocument, api_upload_invoice_worddocument, api_represents_now, api_client, api_represents, api_clients, api_contract, api_Invoice, api_ContractItem, api_Job, api_EmailInvoiceWithoutContract, api_EmailInvoiceFirstWithContract, api_EmailInvoiceOtherInvoicesWithContract,  api_EmailInvoiceReminder, api_EmailInvoiceOnlyOneWithContract, singing_later, api_EmailSubjectforDocuSign#, VueAppView

urlpatterns = [
    #re_path(r'^client/.*$', VueAppView.as_view(), name='vue-app'), #This is for deployment

    path('api/EmailInvoiceWithoutContract/', api_EmailInvoiceWithoutContract, name='api_EmailInvoiceWithoutContract'),
    path('api/EmailInvoiceFirstWithContract/', api_EmailInvoiceFirstWithContract, name='api_EmailInvoiceFirstWithContract'),
    path('api/EmailInvoiceOtherInvoicesWithContract/', api_EmailInvoiceOtherInvoicesWithContract, name='api_EmailInvoiceOtherInvoicesWithContract'),
    path('api/EmailInvoiceReminder/', api_EmailInvoiceReminder, name='api_EmailInvoiceReminder'),
    path('api/EmailInvoiceOnlyOneWithContract/', api_EmailInvoiceOnlyOneWithContract, name='api_EmailInvoiceOnlyOneWithContract'),
    path('api/EmailSubjectforDocuSign/', api_EmailSubjectforDocuSign, name='api_EmailSubjectforDocuSign'),


    path('api/contract/', api_contract, name='api_contract'),
    path('api/invoice/', api_Invoice, name='api_invoice'),
    path('api/contract-item/', api_ContractItem, name='api_contract_item'),
    path('api/jobs/', api_Job, name='api_job'),

    path('api/clients/', api_clients, name='api_clients'),
    path('api/represents/', api_represents, name='api_represents'),
    path('api/client/', api_client, name='api_client'),
    path('api/represents/now/', api_represents_now, name='api_represents_now'),

    path('api/contract-upload/', api_upload_contract_worddocument, name='api_contract_upload'),
    path('api/invoice-upload/', api_upload_invoice_worddocument, name='api_invoice_upload'),

    path('api/contract/signingLater/', singing_later, name='singing_later'),

]
