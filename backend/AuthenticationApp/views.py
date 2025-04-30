from django.http import JsonResponse
from django.utils import timezone
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
from .models import Workplace, Invite
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

#This sets 'User' to be the correct User model (either default or custom)
User = get_user_model()

@csrf_exempt
def register_company(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method rquired'}, status=405)
    
    try:
        data = json.loads(request.body)
        workplace_name = data.get('workplace_name')
        workplace_address = data.get('workplace_address')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not all([workplace_name, workplace_address, username, email, password, first_name, last_name]):
            return JsonResponse({'error': 'All fields required'}, status=400)
        #This creates and insers a new row into the "Workplace" table in the database defined in the models.py file.
        workplace = Workplace.objects.create(name=workplace_name, address=workplace_address)
        #The invite_code is generated automatically using uuid.uuid4() as it was set as default in the models.py file.

        #This creates a new user in the "auth_user" table (or the custom user table (in my case my custom extended table there are two additional fields I added in models.py)).
        #Behind the scenes, this:
        # -Salts and hashes the password using Django's password hashing system (PBKDF2 by default)
        # -Stores username, email, password hash, is_company_admin=True, and company FK
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password, #Django automatically salts and hashes the password inside create_user.
            first_name=first_name,
            first_name=last_name,
            is_company_admin=True,
            workplace=workplace
        )
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'error': str(Exception)}, status=500)



@login_required
def invite_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    email = data.get('email')

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
    invite = Invite.objects.create(email=email, workplace=current_user.workplace)
    #Here I prepare the link for the user to log in with the unique token generated taken from the database.
    invite_link = f"https://myfrontend.com/register?token={invite.token}"
    #Here I send an email to the user.
    send_mail(
        subject="Join your company",
        message=f"You've been invited to join {current_user.workplace.name}. Click here to join the company: {invite_link}",
        from_email = User.workplace.email, #This is just here to fill space, I will need to look into development of secure email login or api infrastructure to use client's email accounts to send emails.
        receipient_list=[email]
    )
    


@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        token = data.get('token')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not all([token, username, email, password, first_name, last_name]):
            return JsonResponse({'error': 'All fields required'}, status=400)
        
        try:
            invite = Invite.objects.get(token=token, is_used=False)
        except Invite.DoesNotExist:
            return JsonResponse({'error': 'Invalid or used invite'}, status=400)
        
        if invite.is_expired():
            return JsonResponse({'error': 'Invite expired'}, status=400)
        
        if invite.email != email:
            return JsonResponse({'error': 'Email does not match invitation'}, status=400)
        
        #Django salts and hashes the password and inserts the user with company FK.
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            workplace=invite.workplace,
            first_name = first_name,
            last_name = last_name
        )

        invite.is_used = True
        invite.save()
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'error': str(Exception)}, status=500)



@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data =json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not all([username, password]):
            return JsonResponse({'error': 'Username and password required'}, status=400)
        #this authenticate() function checks the username and password.
        #It queries the database for a user with the username.
        #It then checks the password hash as part of the function.
        #Returns the User Object if username matches the username in the database and the salt+hash of the password matches the salt+hash of the password in the database, otherwise returns None.
        user = authenticate(username=username, password=password)

        if user:
            #LOGIN:
            #This function login() creates a session for the user (using Django's session middleware)
            #Stores the user's ID in the session (request.session['_auth_user_id'] internally)
            #Attaches the user object to request.user for future requests.
            login(request, user)
            #At this point, Django has:
            #Written the session ID into the browser's cookies (using Set-Cookie)
            #Stored the session info (linked to user ID) in the database by default.
            return JsonResponse({'success': True, 'user': user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception:
        return JsonResponse({'error': str(Exception)}, status=500)



@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        #the logout() function deletes session data from the backend (if using DB sessions, deletes from django_session table)
        #Clears the session ID from the browser's cookies
        #Sets request.user to AnonymousUser
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'POST method required'}, status=405)

