from django.db import models
from AuthenticationApp.models import Workplace, CustomUser
from datetime import timedelta
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
# Create your models here.
#Add the as_dict() methods here to serialise all objects


class Email_Template(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    workplace = models.ForeignKey(Workplace, null = True, blank = True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class EmailInvoiceWithoutContract_individual(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceFirstWithContract_individual(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceOtherInvoicesWithContract_individual(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceReminder_individual(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }


class EmailInvoiceWithoutContract_company(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceFirstWithContract_company(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceOtherInvoicesWithContract_company(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceReminder_company(Email_Template):
    def as_dict(self):
        return{
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceOnlyOneWithContract_company(Email_Template):
    def as_dict(self):
        return {
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailInvoiceOnlyOneWithContract_individual(Email_Template):
    def as_dict(self):
        return {
            'id': self.id,
            'Subject': self.subject,
            'Body': self.body,
        }

class EmailSubjectforDocuSign_company(models.Model):
    subject = models.CharField(max_length=255)
    workplace = models.ForeignKey(Workplace, null = True, blank = True, on_delete=models.CASCADE)
    def as_dict(self):
        return {
            'id': self.id,
            'Subject': self.subject,
        }

class EmailSubjectforDocuSign_individual(models.Model):
    subject = models.CharField(max_length=255)
    workplace = models.ForeignKey(Workplace, null = True, blank = True, on_delete=models.CASCADE)
    def as_dict(self):
        return {
            'id': self.id,
            'Subject': self.subject,
        }
    




class Client(models.Model):
    phone = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    address = models.TextField(null=True)
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True



#Add email address according to the database model
class Client_Individual(Client):
    Fname = models.CharField(max_length=255)
    Lname = models.CharField(max_length=255)

    def as_dict(self):
        return {
            'id': self.id,
            'Fname': self.Fname,
            'Lname': self.Lname,
            'Phone': self.phone,
            'ClientEmail': self.email,
            'address': self.address,
            'ClientType': 'Client_Individual'
        }

#Add email address according to the databse model
class Client_Company(Client):
    name = models.CharField(max_length=255)
    Signer = models.ForeignKey(Client_Individual, on_delete=models.CASCADE, null=True, blank=True)

    def as_dict(self):
        return {
            'id': self.id,
            'CompanyName': self.name,
            'CompanyEmail': self.email,
            'Phone': self.phone,
            'address': self.address,
            'ClientType': 'Client_Company',
            'IndividualId': self.Signer.id if self.Signer else None,
        }

#Here the from_entity is the one doing the representing.
#And to_entity is the one being represented by the from_entity.
class Represents(models.Model):
    from_content_type = models.ForeignKey(
        ContentType, #Django model which stores information about all models
        related_name='represents_from_type',
        null=True,
        on_delete=models.CASCADE)
    from_object_id = models.PositiveIntegerField(null=True,)
    #Combines the from_content type with the from_object id to link to an object in the database
    from_entity = GenericForeignKey('from_content_type', 'from_object_id')

    to_content_type = models.ForeignKey(ContentType, related_name='represents_to_type', null=True, on_delete=models.CASCADE)
    to_object_id = models.PositiveIntegerField(null=True,)
    to_entity = GenericForeignKey('to_content_type', 'to_object_id')

    primary_contact = models.BooleanField(default=True)
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)
    selected = models.BooleanField(default=False)
    #Method which prevents an entity from representing itself.
    #This method is called automatically by Django on creation of an object.
    def clean(self):
        if self.from_content_type == self.to_content_type and self.from_object_id == self.to_object_id:
            raise ValidationError("An entity cannot represent itself.")
        
    def as_dict(self):
        from_entity = self.from_entity
        to_entity = self.to_entity

        data = {
            'primary_contact': self.primary_contact,
            'selected': self.selected,
        }
        if isinstance(from_entity, Client_Individual):
            data.update({
                'from_id': self.from_object_id,
                'from_type': self.from_content_type.model,
                'from_Fname': from_entity.Fname,
                'from_Lname': from_entity.Lname,
            })
        elif isinstance(from_entity, Client_Company):
            data.update({
                'from_id': self.from_object_id,
                'from_type': self.from_content_type.model,
                'from_CompanyName': from_entity.name,
            })
        if isinstance(to_entity, Client_Individual):
            data.update({
                'to_id': self.to_object_id,
                'to_type': self.to_content_type.model,
                'to_Fname': to_entity.Fname,
                'to_Lname': to_entity.Fname,
                'to_Lname': to_entity.Lname,
            })
        elif isinstance(to_entity, Client_Company):
            data.update({
                'to_id': self.to_object_id,
                'to_type': self.to_content_type.model,
                'to_CompanyName': to_entity.name,
            })
        return data
    
class UploadedContractOrInvoiceWordDocument(models.Model):
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract=True

class UploadedContractWordDocumentCompany(UploadedContractOrInvoiceWordDocument):
    file = models.FileField(upload_to="documents/contract/company")

class UploadedContractWordDocumentIndividual(UploadedContractOrInvoiceWordDocument):
    file = models.FileField(upload_to="documents/contract/individual")

class UploadedInvoiceWordDocumentCompany(UploadedContractOrInvoiceWordDocument):
    file = models.FileField(upload_to="documents/invoice/company")

class UploadedInvoiceWordDocumentIndividual(UploadedContractOrInvoiceWordDocument):
    file = models.FileField(upload_to='documents/invoice/individual')




class Contract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    People = models.IntegerField(null=True)
    Completed_Value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    file = models.FileField(upload_to="documents/contracts", null=True)
    signingUrl = models.URLField(null=True, blank=True)
    Signed = models.BooleanField(default=False)
    envelope_id = models.CharField(max_length=255, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)
    client_individual = models.ForeignKey(Client_Individual, null=True, blank=True, on_delete=models.CASCADE)
    client_company = models.ForeignKey(Client_Company,null=True, blank=True, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'status': self.status,
            'Price': self.Price,
            'VAT': self.VAT,
            'Total_Price': self.total_amount,
            'People': self.People,
            'Completed_Value': self.Completed_Value,
            'Paid': self.Paid,
            'signingUrl': self.signingUrl,
            'Signed': self.Signed,
            'envelope_id': self.envelope_id,
            'client_individual': self.client_individual.as_dict() if self.client_individual else None,
            'client_company': self.client_company.as_dict() if self.client_company else None
        }

class Invoice_Summary(models.Model):
    number_of_invoices = models.IntegerField()
    schedule = models.CharField(max_length=255, null=True)
    duration = models.CharField(max_length=255, null=True)
    reminders_count = models.IntegerField(null = True)
    reminders_per = models.CharField(max_length=255, null=True)
    contract = models.ForeignKey(Contract, null=True, on_delete=models.SET_NULL)
    Total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Total_VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Total_with_VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    last_invoice_total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    last_invoice_Total_VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    last_invoice_Total_with_VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateField(auto_now_add=True)
    billed_to_company = models.ForeignKey(Client_Company, null=True, on_delete=models.CASCADE)
    billed_to_individual = models.ForeignKey(Client_Individual, null=True, on_delete=models.CASCADE)

    ContactsCompaniesToBeTod = models.ManyToManyField(Client_Company, through='ContactsCompaniesToBeTodThrough', related_name='ContactsCompaniesToBeTod')
    ContactsIndividualsToBeTod = models.ManyToManyField(Client_Individual, through='ContactsIndividualsToBeTodThrough', related_name='ContactsIndividualsToBeTod')
    ContactsCompaniesToBeCCd = models.ManyToManyField(Client_Company, through='ContactsCompaniesToBeCCdThrough', related_name='ContactsCompaniesToBeCCd')
    ContactsIndividualsToBeCCd = models.ManyToManyField(Client_Individual, through='ContactsIndividualsToBeCCdThrough', related_name='ContactsIndividualsToBeCCd')
    ContactsCompaniesToBeBccd  = models.ManyToManyField(Client_Company, through='ContactsCompaniesToBeBccdThrough', related_name='ContactsCompaniesToBeBccd')
    ContactsIndividualsToBeBccd = models.ManyToManyField(Client_Individual, through='ContactsIndividualsToBeBccdThrough', related_name='ContactsIndividualsToBeBccd')
    UsersToBeTod = models.ManyToManyField(CustomUser, through='UsersToBeTodThrough', related_name='UsersToBeTod')
    UsersToBeCCd = models.ManyToManyField(CustomUser, through='UsersToBeCCdThrough', related_name='UsersToBeCCd')
    UsersToBeBccd = models.ManyToManyField(CustomUser, through='UsersToBeBccdThrough', related_name='UsersToBeBccd')
    MainClientToBeTod = models.BooleanField(default=False)
    MainClientToBeCCd = models.BooleanField(default=False)
    MainClientToBeBccd = models.BooleanField(default=False)


    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)

    def as_dict(self):
        return {
            'number_of_invoices': self.number_of_invoices,
            'schedule': self.schedule,
            'duration': self.duration,
            'reminders_count': self.reminders_count,
            'reminders_per': self.reminders_per,
            'contract': self.contract.as_dict() if self.contract else None,
            'Total_price': self.Total_price,
            'Total_VAT': self.Total_VAT,
            'Total_with_VAT': self.Total_with_VAT,
            'last_invoice_total_price': self.last_invoice_total_price,
            'last_invoice_Total_VAT': self.last_invoice_Total_VAT,
            'last_invoice_Total_with_VAT': self.last_invoice_Total_with_VAT,
            'billed_to_company': self.billed_to_company.as_dict() if self.billed_to_company else None,
            'billed_to_individual': self.billed_to_individual.as_dict() if self.billed_to_individual else None,
        }

class ThroughEmailsContacts(models.Model):
    invoice_summary = models.ForeignKey(Invoice_Summary, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    
    class Meta:
        abstract= True


class ContactsCompaniesToBeTodThrough(ThroughEmailsContacts):
    client_company = models.ForeignKey(Client_Company, on_delete=models.CASCADE)

class ContactsIndividualsToBeTodThrough(ThroughEmailsContacts):
    client_individual = models.ForeignKey(Client_Individual, on_delete=models.CASCADE)

class ContactsCompaniesToBeCCdThrough(ThroughEmailsContacts):
    client_company = models.ForeignKey(Client_Company, on_delete=models.CASCADE)

class ContactsIndividualsToBeCCdThrough(ThroughEmailsContacts):
    client_individual = models.ForeignKey(Client_Individual, on_delete=models.CASCADE)

class ContactsCompaniesToBeBccdThrough(ThroughEmailsContacts):
    client_company = models.ForeignKey(Client_Company, on_delete=models.CASCADE)

class ContactsIndividualsToBeBccdThrough(ThroughEmailsContacts):
    client_individual = models.ForeignKey(Client_Individual, on_delete=models.CASCADE)

class ThroughEmailsUsers(models.Model):
    invoice_summary = models.ForeignKey(Invoice_Summary, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class UsersToBeTodThrough(ThroughEmailsUsers):
    def as_dict():
        return {
            'invoice_summary': self.invoice_summary,
            'user': self.user
        }

class UsersToBeCCdThrough(ThroughEmailsUsers):
    def as_dict():
        return {
            'invoice_summary': self.invoice_summary,
            'user': self.user
        }
class UsersToBeBccdThrough(ThroughEmailsUsers):
    def as_dict():
        return {
            'invoice_summary': self.invoice_summary,
            'user': self.user
        }

class InvoiceItem(models.Model):
    Name = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    invoice_summary = models.ForeignKey(Invoice_Summary, null=True, on_delete=models.SET_NULL)
    last = models.BooleanField(default=False)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, null=True)


    def as_dict(self):
        return {
            'Name': self.Name,
            'Price': self.Price,
            'VAT': self.VAT,
            'Total_price': self.Total_price,
            'last': self.last,
            'invoice_summary': self.invoice_summary.as_dict()
        }

class Invoice(models.Model):
    InvoiceItems = models.ManyToManyField(InvoiceItem, through='InvoicesToInvoiceItems')
    InvoiceSummary = models.ForeignKey(Invoice_Summary, null=True, on_delete=models.SET_NULL)
    contract = models.ForeignKey(Contract, null=True, on_delete=models.SET_NULL)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255)
    Paid = models.BooleanField(default=False)
    Completed_Value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_file = models.FileField(upload_to='documents/invoices', null=True)
    client_company = models.ForeignKey(Client_Company, null=True, on_delete=models.CASCADE)
    client_individual = models.ForeignKey(Client_Individual, null=True, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'id': self.id,
            'identifier': self.identifier,
            'InvoiceSummary': self.InvoiceSummary.as_dict() if self.InvoiceSummary else None,
            'contract': self.contract.as_dict() if self.contract else None,
            'Paid': self.Paid,
            'Completed_Value': self.Completed_Value,
            'filePath': self.invoice_file.url if self.invoice_file else None
        }

class InvoicesToInvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_item = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'id': self.id,
            'invoice': self.invoice.as_dict(),
            'invoice_item': self.invoice_item.as_dict()
        }

class ContractItem(models.Model):
    Name = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Selected_VAT_Rate = models.CharField(max_length=255, null=True)
    Total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    VAT = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'ItemName': self.Name,
            'Price': self.Price,
            'Selected_VAT_Rate': self.Selected_VAT_Rate,
            'Total_price': self.Total_price,
            'VAT': self.VAT,
            'contract': self.contract.as_dict()
        }

class Job(models.Model):
    started_at = models.DateTimeField(null=True)
    status = models.CharField()
    completed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    corresponds_to_ContractItem = models.ForeignKey(ContractItem, null=True, on_delete=models.CASCADE)
    corresponds_to_InvoiceItem = models.ForeignKey(InvoiceItem, null=True, on_delete=models.CASCADE)
    Deadline = models.DateField(null=True)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'id': self.id,
            'ContractItem': self.corresponds_to_ContractItem.as_dict() if self.corresponds_to_ContractItem else None,
            'InvoiceItem': self.corresponds_to_InvoiceItem.as_dict() if self.corresponds_to_InvoiceItem else None,
            'started_at': self.started_at.strftime("%d-%m-%Y") if self.started_at else None,
            'status': self.status,
            'created_at': self.created_at.strftime("%d-%m-%Y") if self.created_at else None,
            'completed_at': self.completed_at.strftime("%d-%m-%Y") if self.completed_at else None,
            'Deadline': self.Deadline.strftime("%d-%m-%Y") if self.Deadline else None,

        }
    
class JobAssigned(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE)
    User = models.ForeignKey('AuthenticationApp.CustomUser', on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, null=True)

    def as_dict(self):
        return {
            'Job': self.Job.as_dict(),
            'User': self.User.as_dict()
        }


