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
from django.urls import path
from .views import base_view, token_confirmation, docusign_callback, Users_view, UserRegistrationPage_view, Email_Confirmation, LandingPage_view, SecurityInfoPage_view, LoginPage_view, SignUpPage_view, EmailConfirmationRegistrationPage_view, register_company, invite_user, register_user, login_user, logout_user, docusign_disconnect, Password_reset_view, Password_reset, Password_reset_confirmation_view, Reset_password, Reset_password_view, Account_Unlocked_view, Account_locked_view, Workplace_api

urlpatterns = [
    #path('', base_view),
    path('', LandingPage_view, name='landing_page'),
    path('SecurityInfoPage/', SecurityInfoPage_view, name='security_info'),
    path('LoginPage/', LoginPage_view, name='login'),
    path('SignUpPage/', SignUpPage_view, name='Sign_Up'),
    path('EmailConfirmationPage/', EmailConfirmationRegistrationPage_view, name='EmailConfirmation'),
    path('api/emailconfirmation/', Email_Confirmation, name="Confirmation_Code"),
    path('UserRegistrationPage/', UserRegistrationPage_view, name="UserRegistrationPage"),
    path('PasswordResetPage/', Password_reset_view, name='password_reset_view'),
    path('PasswordResetConfirmationPage/', Password_reset_confirmation_view, name='password_reset_confirmation_view'),
    path('ResetPasswordPage', Reset_password_view, name="Reset_password_view"),
    path('AccountUnlocked', Account_Unlocked_view, name='AccountUnlockedPage'),
    path('AccountLocked', Account_locked_view, name='AccountLockedPage'),

    path('api/register/company/', register_company, name='register_company'),
    path('api/invite_user', invite_user, name='invite_user'),
    path('api/register_user/', register_user, name='register_user'),
    path('api/login/', login_user, name='loginformsubmit'),
    path('api/logout/', logout_user, name='logoutformsubmit'),
    path('api/Users/', Users_view, name='Users'),
    path('api/Password_Reset/', Password_reset, name='Password_reset'),
    path('api/ResetPassword/', Reset_password, name='Reset_password'),

    path('api/docusign/callback/', docusign_callback, name='docusign_callback'),
    path('api/token_confirmation/', token_confirmation, name='token_confirmation'),
    path('api/docusign/disconnect/', docusign_disconnect, name='docusign_disconnect'),

    path('api/workplace/', Workplace_api, name='Workplace'),
]
