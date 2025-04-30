from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class Workplace(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #the UUIDField stands for Universally Unique Identifier
    #it is a 128-bit number used to uniquely identify things.
    #I used it to generate an invite code because I need it to be:
    #Unique across all companies and for all users,
    #Hard to guess (security).
    #invite_code = models.UUIDField(default=uuid.uuid4, unique=True)
    #The default=uuid.uuid4 generate a new UUID every time a Company is created.
    #unique=True basically checks that no two companies can have the same invite code.
    def __str__(self):
        return self.name

#Django provides a built-in User model for authentication.
#But here I want to customise it to suit my own invented authentication model like add new fields to it.
#I can't directly change the built-in User model but django lets me extend it.
#I can therefore create a custom user authentication model in the databse with the extra fields by inheriting AbstractUser class.
class CustomUser(AbstractUser):
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)
    is_company_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_Add=True)
#This CustomUser includes everything Django's default User model has: username, password email etc...
#But plus my fields: workplace, is_company_admin, created_at.
#In the settings.py file I tell Django to use my custom model.

class Invite(models.Model):
    email = models.EmailField()
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_Add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at +timedelta(days=1)
    
    