from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from datetime import timedelta
from django.utils import timezone

# Create your models here.
#Wrokplace model used to store details of the shared company account when it is registered
class Workplace(models.Model):
    name = models.CharField(max_length=255)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField()
    City = models.TextField()
    Zip = models.TextField()
    Country = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
#This CustomUserManager Avoids requiring username.
#The **extra fields, in the self.model allows the CustomUser to save things to the extra attributes each user has.
class CustomUserManager(BaseUserManager):
    #This method is used by Django when creating a normal user (not a superuser)
    def create_user(self, email, password=None, **extra_fields):
        #Make sure an email is provided; it's required since we removed 'username'
        if not email:
            raise ValueError("The Email must be set")
        #Normalises the email (e.g., lowercases domain part of email)
        email = self.normalize_email(email)
        #Creates a new user instance without saving it to the DB yet
        #'self.model'points to the CustomUser model
        user = self.model(email=email, **extra_fields)
        #Hashes and securely stores the password
        user.set_password(password)
        #Saves the user to the database
        user.save()
        return user
    #This method is used when creating a superuser using 'createsuperuser'
    def create_superuser(self, email, password=None, **extra_fields):
        #These fields must be True for a superuser account
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        #If any of the required flags are not set correctly, raises an error
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Suprtuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        #Uses the create_user method to actually create the user.
        return self.create_user(email, password, **extra_fields)

#Invite object to store data about a user being invited to the shared workplace database
class Invite(models.Model):
    email = models.EmailField()
    Fname = models.CharField(max_length=255, null=True)
    Lname = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    Admin = models.BooleanField(default=False)
    #the UUIDField stands for Universally Unique Identifier
    #it is a 128-bit number used to uniquely identify things.
    #Used here to generate an invite token because it needs to be:
    #Unique across all companies and for all users,
    #Hard to guess (security).
    #The default=uuid.uuid4 generate a new UUID every time a Company is created.
    #unique=True basically checks that no two invite objects can have the same invite code.
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    #Used to check if the invite token is expired (security) is set the expiry time to one day (personal choice)
    def is_expired(self):
        return timezone.now() > self.created_at +timedelta(days=1)
    
    def as_dict(self):
        return {
            "id": self.id,
            "Fname": self.Fname,
            "Lname": self.Lname,
            "email": self.email,
            "position": self.position,
            "Company_Admin": self.Admin,
        }
    


#Django provides a built-in User model for authentication.
#But here I want to customise it to suit my own invented authentication model like add new fields to it.
#I can't directly change the built-in User model but django lets me extend it.
#I can therefore create a custom user authentication model in the databse with the extra fields by inheriting the AbstractUser class.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None #Removes default username field
    USERNAME_FIELD = 'email' #Uses email to log in
    REQUIRED_FIELDS = ['first_name', 'last_name'] #
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=255, null=True)
    superuser = models.BooleanField(default=False)
    is_company_admin = models.BooleanField(default=False)
    email_confirmation_code = models.TextField(null=True)
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    invite = models.ForeignKey(Invite, null=True, blank=True, on_delete=models.SET_NULL)
    jobs = models.ManyToManyField('MainApp.Job', through='MainApp.JobAssigned', null=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    unlock_account_token = models.UUIDField(null=True, unique=True)
    unlock_account_token_created_at = models.DateTimeField(null=True)
    unlock_account_token_expires_at = models.DateTimeField(null=True)
    reset_password_token = models.UUIDField(default=uuid.uuid4, unique=True)
    reset_password_token_created_at = models.DateTimeField(null=True)
    reset_password_token_expires_at = models.DateTimeField(null=True)
#This CustomUser includes everything Django's default User model has: username, password email etc...
#But plus my fields: workplace, is_company_admin, created_at.
#In the settings.py file I tell Django to use my custom model.
    objects = CustomUserManager() #Applies my manager.

    def as_dict(self):
        return {
            "id": self.id,
            "Fname": self.first_name,
            "Lname": self.last_name,
            "email": self.email,
            "position": self.position,
            "Company_Admin": self.is_company_admin,
            "email_confirmed": self.email_confirmed,
            "failed_login_attempts": self.failed_login_attempts,
            "last_failed_login": self.last_failed_login,
            "superuser": self.superuser,
            "is_locked": self.is_locked
            #"jobs": self.jobs,
        }
    
#Model used to store DocuSign account details and the token to access and refresh the access token to the account
class DocuSignToken(models.Model):
    workplace = models.OneToOneField(Workplace, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()
    scope = models.TextField()
    account_id = models.CharField(max_length=255, blank=True, null=True)
    base_uri = models.URLField(blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)
    user_full_name = models.CharField(max_length=255, blank=True, null=True)
