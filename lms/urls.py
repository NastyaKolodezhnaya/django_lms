"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from users.views import IndexPage
from django.conf.urls.static import static
from django.conf import settings

from users.views import LoginUser, LogoutUser, UserSignIn, RegistrationUser, ActivateUser

from users.views import handle_error_404
from django.conf.urls import handler404


urlpatterns = [
    path('', IndexPage.as_view(), name='start'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('authentication', include('social_django.urls', namespace='social')),

    path('users/', include('users.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'users.views.handle_error_404'
