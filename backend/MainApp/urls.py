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
from django.contrib import admin
from django.urls import path
from views import api_email_template_first, api_email_template_second, api_client_individual, api_client_company, api_contract, api_Recurring_Invoice, api_Invoice, api_ContractItem, api_Job

urlpatterns = [
    path('api/email-template-first/', api_email_template_first, name='api_email_template_first'),
    path('api/email-template-second/', api_email_template_second, name='api_email_template_second'),
    path('api/client-individual/', api_client_individual, name='api_client_individual'),
    path('api/client-company/', api_client_company, name='api_client_company'),
    path('api/contract/', api_contract, name='api_contract'),
    path('api/recurring-invoice/', api_Recurring_Invoice, name='api_recurring_invoice'),
    path('api/invoice/', api_Invoice, name='api_invoice'),
    path('api/contract-item/', api_ContractItem, name='api_contract_item'),
    path('api/job', api_Job, name='api_job'),


]
