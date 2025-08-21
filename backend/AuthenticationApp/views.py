from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
#These are the main functions of Django's authentication system.
#'authenticate' checks credentials and returns a user object if valid.
#'login' attaches the user to the session (logs them in)
#'logout' removes the user from the session (logs them out)
from django.contrib.auth import authenticate, login, logout
#The login_required decorator does the following:
#If the user isn't logged in, it redirects the user to settings.LOGIN_URL, passing the path specified by setting.Login_URL in the browser.
#If the user is logged in, it executes the view normally. The view code is then free to assume the user is logged in because the decorator does all the checking and security.
from django.contrib.auth.decorators import login_required
#This is how Django allows me to work with the currently configured User model (default or custom)
#It avoids hardcoding the import like 'from django.contrib.auth.models import User'
#If I later switch to a custom user model (like CustomUser), this automatically uses it.
from django.contrib.auth import get_user_model
from .models import Workplace, Invite, DocuSignToken, CustomUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import pycountry
import random
import requests
from urllib.parse import urlencode
import uuid
# Create your views here.

#This sets 'User' to be the correct User model (either default or custom)
User = get_user_model()

#Below are view functions that render django templates:
@csrf_exempt
def base_view(request):
    return render(request, "AuthenticationApp/base.html")

@csrf_exempt
def LandingPage_view(request):
    return render(request, "AuthenticationApp/LandingPage.html")

@csrf_exempt
def SecurityInfoPage_view(request):
    return render(request, "AuthenticationApp/SecurityInfoPage.html")

@csrf_exempt
def LoginPage_view(request):
    return render(request, "AuthenticationApp/LoginPage.html")

@csrf_exempt
def Password_reset_view(request):
    return render(request, "AuthenticationApp/PasswordResetPage.html")

@csrf_exempt
def Password_reset_confirmation_view(request):
    return render(request, f"AuthenticationApp/PasswordResetConfirmationPage.html")

@csrf_exempt
def Reset_password_view(request):
    token = request.GET.get('token')
    return render(request, "AuthenticationApp/ResetPasswordPage.html", {'token': token})

@csrf_exempt
def Account_locked_view(request):
    return render(request, "AuthenticationApp/AccountLocked.html")

@csrf_exempt
def Account_Unlocked_view(request):
    #This gets the unlock token from the url of the page
    token = request.GET.get('token')
    #Gets the user object the token is an attribute of
    user = CustomUser.objects.get(unlock_account_token = token)
    #If a valid user object is returned and the unlock token expity date is past the time this request is made the account gets unlocked
    if user.unlock_account_token_expires_at >= timezone.now():
        user.is_locked = False
        user.failed_login_attempts = 0
        user.unlock_account_token = None
        user.unlock_account_token_created_at = None
        user.unlock_account_token_expires_at = None
        user.save()
        return render(request, "AuthenticationApp/AccountUnlocked.html", {'token': token})
    #If a valid user object is returned but the unlock token expiry date is before the time this request is made a new token gets created,
    #A new expiry date is sent for the token (15 minues after creation) (security)
    #A new link with the new token is sent to the users account email to unlock their account.
    else:
        token = uuid.uuid4()
        email = user.email
        user.unlock_account_token = token
        user.unlock_account_token_created_at = timezone.now()
        user.unlock_account_token_expires_at = user.unlock_account_token_created_at + timedelta(minutes=15)
        link = f"http://localhost:8000/AccountUnlocked?token={token}"
        send_mail(
            subject="Unlock your account",
            message=f"The last link has expired, please follow this link to unlock your account: {link}. \n \nThis link is valid for 15 minutes.",
            from_email=None,
            #from_email = User.workplace.email, #This is just here to fill space, I will need to look into development of secure email login or api infrastructure to use client's email accounts to send emails.
            recipient_list=[email],
            fail_silently=False
            )
        return Account_locked_view(request)


@csrf_exempt
def SignUpPage_view(request):
    countries = [country.name for country in pycountry.countries]
    return render(request, "AuthenticationApp/SignUpPage.html", {'countries': countries})

def EmailConfirmationRegistrationPage_view(request):
    user_id = request.GET.get('user_id')
    return render(request, "AuthenticationApp/EmailConfirmationRegistrationPage.html", {'user_id': user_id})

def UserRegistrationPage_view(request):
    token = request.GET.get('token')
    invite = Invite.objects.get(token=token, is_used=False)
    if not invite:
        return JsonResponse({'Token: Invalid'})
    return render(request, "AuthenticationApp/UserRegistrationPage.html", {'invite': invite})


@csrf_exempt
def register_company(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method rquired'}, status=405)
    
    try:
        workplace_name = request.POST.get('workplace_name')
        workplace_address_line_1 = request.POST.get('workplace_address_line_1')
        workplace_address_line_2 = request.POST.get('workplace_address_line_2')
        workplace_address_city = request.POST.get('workplace_address_city')
        workplace_address_Zip = request.POST.get('workplace_address_Zip')
        workplace_address_Country = request.POST.get('workplace_address_Country')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not all([workplace_name, workplace_address_line_1, workplace_address_line_2, workplace_address_city, workplace_address_Zip, workplace_address_Country,  email, password, first_name, last_name]):
            return JsonResponse({'error': 'All fields required'}, status=400)
        #This creates and insers a new row into the "Workplace" table in the database defined in the models.py file.
        workplace = Workplace.objects.create(name=workplace_name, address_line_1 = workplace_address_line_1, address_line_2 = workplace_address_line_2, City = workplace_address_city, Zip = workplace_address_Zip, Country = workplace_address_Country)
        #The invite_code is generated automatically using uuid.uuid4() as it was set as default in the models.py file.

        #This creates a new user in the "auth_user" table (or the custom user table (in my case my custom extended table there are two additional fields I added in models.py)).
        #Behind the scenes, this:
        # -Salts and hashes the password using Django's password hashing system (PBKDF2 by default)
        # -Stores username, email, password hash, is_company_admin=True, and company FK
        Confirmation_code = random.randrange(100000, 999999)
        user = User.objects.create_user(
            email=email,
            password=password, #Django automatically salts and hashes the password inside create_user.
            first_name=first_name,
            last_name=last_name,
            is_company_admin=True,
            workplace=workplace,
            email_confirmation_code=Confirmation_code,
            superuser = True
        )
        #Confirmation_code_email = EmailMessage(
        #    "Confirmation Code",
        #    f"Dear {user.first_name}, Here is your confirmation code: {random.randrance(100000, 999999)}"
        #)
        send_mail(
            subject="Confirmation Code",
            message=f"Dear {user.first_name}, Here is your confirmation code: {user.email_confirmation_code}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        user_id = user.id

        return redirect(f"/EmailConfirmationPage/?user_id={user_id}")
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def Email_Confirmation(request):
    #Continues with the PUT simulation by checking that the input tag's value is PUT:
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        try:
            user_id = request.GET.get('user')
            user_id = int(user_id)
            confirmation_code = request.POST.get('confirmation_code')
            user = User.objects.get(email_confirmation_code = confirmation_code, id = user_id)
            if user:
                user.email_confirmed = True
                user.save()
                return redirect(f"/LoginPage/")
            else:
                return redirect(f"/EmailConfirmationPage/?user_id={user_id}&error=invalid")
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'PUT method rquired'}, status=405)
    

@csrf_exempt
@login_required
def invite_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    Fname = data.get('Fname')
    Lname = data.get('Lname')
    email = data.get('email')
    position = data.get('position')
    Company_Admin = data.get('Company_Admin')

    #request.user is the currently authenticated user (based on session or token)
    #request.user is the currently logged-in user, added automatically to each request.
    #Provided by Django's AuthenticationMiddleware.
    #It's either:
    #An instance of my CustomUser (if authenticated), or
    #An instance of AnonymousUser (if not authenticated)
    #In my case it's always going to be an instance of my CustomUser because of the @login_required decorator.
    current_user = request.user
    #When a user logs in using Django's login(request, user), Django creates a session.
    #That session stores the user ID.
    #On the next request, the middleware reads that session and sets request.user with the session id.

    #This requires the user to be authenticated beforehand
    #Django sets request.user automatically via AuthenticationMiddleware
    #If not logged in, request.user will be an instance of AnonymousUser which can't be in my case because of the decorator.
#    if not current_user.is_authenticated:
#        return JsonResponse({'error': 'Authentication required'}, status=401)
    #I assume that the logged-in user is already part of a company
    if not current_user.workplace:
        return JsonResponse({'error': 'No company found for current user'}, status=403)
    #Here I create the invite and store it in the database.
    invite = Invite.objects.create(Fname = Fname, Lname = Lname, email=email, position=position, workplace=current_user.workplace, Admin=Company_Admin)
    #Here I prepare the link for the user to log in with the unique token generated taken from the database.
    invite_link = f"http://localhost:8000/UserRegistrationPage/?token={invite.token}"
    #Here I send an email to the user.
    #Send the invite email from my app email, not from the user's email.
    send_mail(
        subject="Join your company",
        message=f"You've been invited to join {current_user.workplace.name}. Click here to join the company: {invite_link}",
        from_email=None,
#        from_email = User.workplace.email, #This is just here to fill space, I will need to look into development of secure email login or api infrastructure to use client's email accounts to send emails.
        recipient_list=[email],
        fail_silently=False
    )
    return JsonResponse(invite.as_dict())


@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        token = request.GET.get('token') #Here I use a .GET method to get the token because it contains query string parameters (from the URL, after the ?).
        #.POST contains the form data sent via the body of a POST request.
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not all([token, email, password, first_name, last_name]):
            return JsonResponse({'error': 'All fields required'}, status=400)
        
        try:
            invite = Invite.objects.get(token=token, is_used=False)
        except Invite.DoesNotExist:
            return JsonResponse({'error': 'Invalid or used invite'}, status=400)
        
        if invite.is_expired():
            return JsonResponse({'error': 'Invite expired'}, status=400)
        
        if invite.email != email:
            return JsonResponse({'error': 'Email does not match invitation'}, status=400)
        
        if invite.Fname.lower() != first_name.lower() or invite.Lname.lower() != last_name.lower():
            return JsonResponse({'error': "First Name and/or Last Name don't match the invited user's First Name and/or Last Name"})
        #Sets an easy to type in confirmation code
        Confirmation_code = random.randrange(100000, 999999)
        is_company_admin = invite.Admin
        position = invite.position
        #Django salts and hashes the password and inserts the user with company FK.
        user = User.objects.create_user(
            email=email,
            password=password,
            workplace=invite.workplace,
            first_name = first_name,
            last_name = last_name,
            email_confirmation_code=Confirmation_code,
            is_company_admin= is_company_admin,
            position=position,
            invite=invite,
        )

        invite.is_used = True
        invite.save()

        send_mail(
            subject="Confirmation Code",
            message=f"Dear {user.first_name}, Here is your confirmation code: {user.email_confirmation_code}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )

        user_id = user.id
        return redirect(f"/EmailConfirmationPage/?user_id={user_id}")
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([email, password]):
            return redirect(f"/LoginPage/?error=invalid")
        #this authenticate() function checks the username and password.
        #It queries the database for a user with the username.
        #It then checks the password hash as part of the function.
        #Returns the User Object if username matches the username in the database and the salt+hash of the password matches the salt+hash of the password in the database, otherwise returns None.
        user = authenticate(email=email, password=password)

        if user:
            if user.email_confirmed:
            #LOGIN:
            #This function login() creates a session for the user (using Django's session middleware)
            #Stores the user's ID in the session (request.session['_auth_user_id'] internally)
            #Attaches the user object to request.user for future requests.
                login(request, user)
            #At this point, Django has:
            #Written the session ID into the browser's cookies (using Set-Cookie)
            #Stored the session info (linked to user ID) in the database by default.
            #Here instead of returning success, I redirect the user to the Vue app.
                if user.failed_login_attempts > 0:
                    user.failed_login_attempts = 0
                    user.save()
                return redirect('http://localhost:5173/')
                #return redirect("/app/") #This is for redirecting in production
            else:
                send_mail(
                    subject="Confirmation Code",
                    message=f"Dear {user.first_name}, Here is your confirmation code: {user.email_confirmation_code}",
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                user_id = user.id
                return redirect(f"/EmailConfirmationPage/?user_id={user_id}")
        else:
            #This handles failed login attempts and locking of the account. On 5 wrong login attempts the account gets locked.
            user = CustomUser.objects.get(email = email)
            if user.failed_login_attempts <= 4:
                user.failed_login_attempts += 1
                user.save()
            else:
                user.is_locked = True
                token = uuid.uuid4()
                user.unlock_account_token = token
                user.unlock_account_token_created_at = timezone.now()
                user.unlock_account_token_expires_at = user.unlock_account_token_created_at + timedelta(minutes=15)
                user.save()
                link = f"http://localhost:8000/AccountUnlocked?token={token}"
                send_mail(
                    subject="Unlock your account",
                    message=f"Please follow this link to unlock your account: {link}. \n \nThis link is valid for 15 minutes.",
                    from_email=None,
                    #from_email = User.workplace.email, #This is just here to fill space, I will need to look into development of secure email login or api infrastructure to use client's email accounts to send emails.
                    recipient_list=[email],
                    fail_silently=False
                )
                return redirect (f"/AccountLocked")

            return redirect(f"/LoginPage/?error=invalid")
    except Exception as e:
        return redirect(f"/LoginPage/?error=invalid")

#Function which handles requests to reset the password
@csrf_exempt
def Password_reset(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    email = request.POST.get('email')
    if not email:
        print("No email provided in POST data")
        return JsonResponse({'error': 'Email required'}, status=400)
    print(f"Email received: {email}")
    try:
        user = CustomUser.objects.get(email = email)
        print(f"User found: {user}")
    except CustomUser.DoesNotExist:
        print(f"User not found")
        return JsonResponse({'error': 'user not found'})
    token = uuid.uuid4()
    user.reset_password_token = token
    user.reset_password_token_created_at = timezone.now()
    user.reset_password_token_expires_at = user.reset_password_token_created_at + timedelta(minutes=15)
    user.save()
    link = f"http://localhost:8000/ResetPasswordPage?token={token}"

    send_mail(
        subject="Reset your password",
        message=f"Please follow this link to change the password for your account: {link}. \n \n This link is valid for 15 minutes, please make a new password change request if you don't use it in time.",
        from_email=None,
        #from_email = User.workplace.email, #This is just here to fill space, I will need to look into development of secure email login or api infrastructure to use client's email accounts to send emails.
        recipient_list=[email],
        fail_silently=False
    )
    return Password_reset_confirmation_view(request)


#Function resets the function
@csrf_exempt
def Reset_password(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    try:
        token = request.GET.get('token')
        user = CustomUser.objects.get(reset_password_token=token)
        if user.reset_password_token_expires_at >= timezone.now():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return redirect(f"/LoginPage/")
        else:
            email = user.email
            token = uuid.uuid4()
            user.reset_password_token = token
            user.reset_password_token_created_at = timezone.now()
            user.reset_password_token_expires_at = user.reset_password_token_created_at + timedelta(minutes=15)
            user.save()
            link = f"http://localhost:8000/ResetPasswordPage?token={token}"
            send_mail(
                subject="Reset your password",
                message=f"Please follow this link to change the password for your account: {link}. \n \n This link is valid for 15 minutes, please make a new password change request if you don't use it in time.",
                from_email=None,
                #from_email = User.workplace.email, #This is just here to fill space, I will need to look into development of secure email login or api infrastructure to use client's email accounts to send emails.
                recipient_list=[email],
                fail_silently=False
            )
            return JsonResponse({'error': 'Password Link Expired'}, status=401)
    except:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
        




@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        #the logout() function deletes session data from the backend
        #Clears the session ID from the browser's cookies
        #Sets request.user to AnonymousUser
        try:
            #This deletes the session id from the databse.
            request.session.flush()
            #This sets the user to anonymous.
            logout(request)
        except Exception as e:
            return JsonResponse({'Error': str(e)})
        response = JsonResponse({'success': True})
        #This deletes the cookie from the frontend.
        response.delete_cookie('sessionid')
        return response
    return JsonResponse({'error': 'POST method required'}, status=405)

#Function used to get data about users in the shared company workplace, and delete them from the shared company workplace.
#As this is a prototype web application, anyone can delete users.
#Any users can be deleted except for the user that created the company account originally. (The delete button for this user is disabled on the front end)
#Because this is a prototype web application, this is how this prototype currently works.
@csrf_exempt
@login_required
def Users_view(request):
    if request.method == 'GET':
        #Different types of users based on whether they are invited, active and inactive are sent to the front end.
        #The front ends colour codes them into different colous based on which type of user they are for information purposes.
        Invited_Users = [
            {**user.as_dict()}
            for user in Invite.objects.filter(workplace = request.user.workplace, is_used = False)
        ]
        Active_Users = [
            {**user.as_dict()}
            for user in User.objects.filter(workplace = request.user.workplace, email_confirmed = True)
        ]
        Inactive_Users = [
            {**user.as_dict()}
            for user in User.objects.filter(workplace = request.user.workplace, email_confirmed = False)
        ]

        return JsonResponse({'Invited_Users': Invited_Users, 'Active_Users': Active_Users, 'Inactive_Users': Inactive_Users})
    #Delets a user from the shared company database
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        source = data.get('source')
        if source == 'invited':
            user_delete = Invite.objects.get(id=id, workplace=request.user.workplace)
            user_delete.delete()
            return JsonResponse({'DELETE': 'Successful'})
        else:
            user_delete = User.objects.get(id=id, workplace=request.user.workplace)
            invite_delete = user_delete.invite
            if invite_delete is not None:
                invite_delete.delete()
            user_delete.delete()
            return JsonResponse({'DELTE': 'Successful'})



#This is a docusign callback function
#This function handles the redirect from DocuSign after the user authenticates their account with my web application.
@login_required
def docusign_callback(request):
    code = request.GET.get('code') #gets the code url parameter from the redirect url returned by DocuSign after authentication
    token_url = "https://account-d.docusign.com/oauth/token" #DocuSign API URL to request an authentication token from docusign for the authenticated account to use for sending enveloped through the connected account
    #Payload of the request to be sent to DocuSign URL above to request the authentication token for the DocuSign account with the code sent by DocuSign for the account
    payload = {
        'grant_type': 'authorization_code', 
        'code': code,
        'redirect_uri': 'http://localhost:8000/api/docusign/callback/',
    }
    #My DocuSign developer account credentials to hit DocuSigns api
    auth = (settings.DOCUSIGN_CLIENT_ID, settings.DOCUSIGN_CLIENT_SECRET)
    #Header to tell DocuSign the content type
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #Sends a post resuest to DocuSign api to exchange the authorisation code for authentication token for the account and refresh tokens to be used to refresh the the authentication token as they expire every 8 hours (DocuSign rule)
    response = requests.post(token_url, data=payload, auth=auth, headers=headers)
    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token'] #Retrieves the account access token to be used for API calls to send envelopes through the connected account
        refresh_token = data.get('refresh_token') #Retrieves the refresh token to be used to request 
        expires_in = int(data['expires_in']) #Retrieves in how much time the current access token expires
        scope = data.get('scope', '') #Retrieves the permissions given by DocuSign

        expires_at = timezone.now() + timedelta(seconds=expires_in) #Calculates the expiry date and time of the access token
        #Requests user information from DocuSign using the access token (Some of it is needed for me to build the request payloads for making DocuSign API calls (refer to MainApp.views api_contract function))
        userinfo_url = "https://account-d.docusign.com/oauth/userinfo"
        userinfo_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        userinfo_response = requests.get(userinfo_url, headers=userinfo_headers)
        #In case the request failed, redirects to the front end telling it that docusign account has failed to authenticate
        if userinfo_response.status_code != 200:
            return redirect('http://localhost:5173/?success=false')
        #Extracts the response data from docusign
        userinfo = userinfo_response.json()
        account_info = userinfo['accounts'][0] #Gets the authenticated account
        account_id = account_info['account_id'] #Gets the authenticated DocuSign account ID
        base_uri = account_info['base_uri'] #Gets the url to be used for making api calls to DocuSign
        #Extracts DocuSign account holder details from the response
        user_email = userinfo.get("email")
        given_name = userinfo.get("given_name", "")
        family_name = userinfo.get("family_name", "")
        user_full_name = f"{given_name} {family_name}".strip()
        #Saves or updated the DocuSignToken object with the extracted data from responses in the database for this workplace
        DocuSignToken.objects.update_or_create(
            workplace=request.user.workplace,
            defaults={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': expires_at,
                'scope': scope,
                'account_id': account_id,
                'base_uri': base_uri,
                'user_email': user_email,
                'user_full_name': user_full_name
            }
        )
        #Redirects the user to frontend telling it the authentication was successful
        return redirect('http://localhost:5173/?success=true')
    #Redirects the user to frontend telling it the authentication wasn't successful
    else:
        return redirect('http://localhost:5173/?success=false')
    
#Function to get a valid DocuSin access token for the account.
def get_valid_docusign_token(workplace):
    token_obj = DocuSignToken.objects.get(workplace=workplace)
    #Checks is the current access token for the account in the database is expired and requests a new token if it has using the refresh token extracted in the function above
    if token_obj.expires_at <= timezone.now():
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': token_obj.refresh_token,
        }

        auth = (settings.DOCUSIGN_CLIENT_ID, settings.DOCUSIGN_CLIENT_SECRET)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_url = "https://account-d.docusign.com/oauth/token"

        response = requests.post(token_url, data=payload, auth=auth, headers=headers)

        if response.status_code == 200:
            data = response.json()
            token_obj.access_token = data['access_token']
            token_obj.refresh_token = data.get('refresh_token', token_obj.refresh_token) # fallback if not rotated
            token_obj.expires_at = timezone.now() + timedelta(seconds=int(data['expires_in']))
            token_obj.scope = data.get('scope', token_obj.scope)
            token_obj.save()
        else:
            raise Exception("Failed to refresh DocuSign token")
    #Returns the current token in the database if the current access token for the account in the database isn't expired
    return token_obj.access_token

#This function tells the frontend whether the DocuSign account for the workplace the request is made from is connected to the web application account or not using the function above
@login_required
def token_confirmation(request):
    if request.method == 'GET':
        if DocuSignToken.objects.filter(workplace=request.user.workplace).exists():
            get_valid_docusign_token(workplace=request.user.workplace)
            return JsonResponse({'connected': True})
        else:
            return JsonResponse({'connected': False})

#This function handles client request to disconnect their DocuSign account from my web app
@csrf_exempt
@login_required
def docusign_disconnect(request):
    if request.method == 'POST':
        token = DocuSignToken.objects.filter(workplace=request.user.workplace)
        #Just deletes the DocuSign Token object for this account.
        if token.exists():
            token.delete()
            return JsonResponse({'message': 'Successfully disconnected from DocuSign'}, status=200)

#This function handles retrieval of the shared company account details to the front end            
@csrf_exempt
@login_required
def Workplace_api(request):
    if request.method == 'GET':
        workplace = request.user.workplace
        return JsonResponse(workplace.as_dict())