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
from students.views import IndexPage
from django.conf.urls.static import static
from django.conf import settings

from students.views import LoginStudent, LogoutStudent, StudentSignIn, RegistrationStudent, ActivateUser


urlpatterns = [
    path('', IndexPage.as_view(), name='start'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('authentication', include('social_django.urls'), name='social'),

    path('sign_in/', StudentSignIn.as_view(), name='sign_in'),
    path('registration/', RegistrationStudent.as_view(), name='registration'),
    path('login/', LoginStudent.as_view(), name='login'),
    path('logout/', LogoutStudent.as_view(), name='logout'),
    path('activate/<str:uidb64>/<str:token>', ActivateUser.as_view(), name='activate'),

    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
