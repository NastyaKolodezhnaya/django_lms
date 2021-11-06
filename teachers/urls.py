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
from django.urls import path
from teachers.views import GetTeachers, CreateTeacher, UpdateTeacher, DeleteTeacher, search_teachers


app_name = 'teachers'

urlpatterns = [
    path('', GetTeachers.as_view(), name='list'),
    path('search', search_teachers, name='search'),
    path('create/', CreateTeacher.as_view(), name='create'),
    path('edit/<pk>/', UpdateTeacher.as_view(), name='edit'),
    path('delete/<pk>/', DeleteTeacher.as_view(), name='delete')
]
