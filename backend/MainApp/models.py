from django.db import models
from AuthenticationApp.models import Workplace, CustomUser
from datetime import timedelta
from django.utils import timezone
# Create your models here.
#Add the as_dict() methods here to serialise all objects
class Email_Template_first(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)

    def as_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'body': self.body,
        }



class Email_Template_second(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)

    def as_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'body': self.body,
        }

#Add email address according to the database model
class Client_Individual(models.Model):
    Fname = models.CharField(max_length=255)
    Lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)

    def as_dict(self):
        return {
            'id': self.id,
            'Fname': self.Fname,
            'Lname': self.Lname,
            'phone': self.phone,
            'address': self.address,
        }

#Add email address according to the databse model
class Client_Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)
    client_individuals = models.ManyToManyField(Client_Individual, through='Represents')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

#Here I model the N-M relationship liking the two tables above, have a look, different from normal sql.
class Represents(models.Model):
    client_individual = models.ForeignKey(Client_Individual, on_delete=models.CASCADE)
    client_company = models.ForeignKey(Client_Company, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)
    primary_contact = models.BooleanField(default=True)

    def as_dict(self):
        return {
            'primary_contact': self.primary_contact
        }

class Contract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BinaryField(default=False)
    total_amount = models.DecimalField()
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)
    client_individual = models.ForeignKey(Client_Individual, on_delete=models.CASCADE)
    client_company = models.ForeignKey(Client_Company, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'created_at': self.created_at,
            'status': self.status,
            'total_amount': self.total_amount
        }

class Recurring_Invoice(models.Model):
    duration = models.DurationField()
    frequency = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'duration': self.duration,
            'frequency': self.frequency
        }

class Invoice(models.Model):
    total_amount = models.IntegerField()
    recurrence = models.ForeignKey(Recurring_Invoice, on_delete=models.CASCADE)
    billed_to_company = models.ForeignKey(Client_Company, on_delete=models.CASCADE)
    billed_to_individual = models.ForeignKey(Client_Individual, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, null = True, blank=True, on_delete=models.SET_NULL)

    def as_dict(self):
        return {
            'total_amount': self.total_amount,
            'recurrence': self.recurrence
        }

class ContractItem(models.Model):
    ItemName = models.CharField(max_length=255)
    description = models.TextField(null=True)
    amount = models.DecimalField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    is_in = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'ItemName': self.ItemName,
            'description': self.description,
            'amount': self.amount
        }

class Job(models.Model):
    ItemName = models.CharField(max_length=255)
    description = models.TextField(null=True)
    started_at = models.DateTimeField()
    status = models.CharField()
    completed_at = models.DateTimeField()
    corresponds_to = models.ForeignKey(ContractItem, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'ItemName': self.ItemName,
            'description': self.description,
            'started_at': self.started_at,
            'status': self.completed_at
        }

