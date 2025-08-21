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
#URL patters to route client requests to either the AuthenticationApp or MainApp router
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #Here I include the default path to my AuthenticationApp.urls.
    path('', include('AuthenticationApp.urls')),
    path('main/', include('MainApp.urls')),
    #path('app/', login_required(TemplateView.as_view(template_name="MainApp/spa/index.html")), name='spa-entry'),
    #re_path(r'^app/(?!api/).*$', login_required(TemplateView.as_view(template_name="MainApp/spa/index.html"))),
]
#This generates url patters that serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#I am going to need another path entry that returns the html index template from vue.