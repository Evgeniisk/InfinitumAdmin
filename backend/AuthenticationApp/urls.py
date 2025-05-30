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
from views import register_company, invite_user, register_user, login_user, logout_user

urlpatterns = [
    path('api/register/company/', register_company),
    path('api/invite/user/', invite_user),
    path('api/register/user/', register_user),
    path('api/login/', login_user),
    path('api/logout/', logout_user),
]
