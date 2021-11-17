from .models import UserProfile, CustomUser, Student
from courses.models import Course

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    ordering = ['last_name']

    list_display = ['first_name', 'last_name', 'email', 'course_applied', 'birthdate']
    list_filter = ['course']
    search_fields = ['first_name__icontains', 'last_name__icontains',
                     'email__icontains', 'course__name__icontains']

    def course_applied(self, instance):
        if instance.course:
            course = instance.course
            return format_html(
                f'<a href="http://127.0.0.1:8000/admin/courses/course/{course.pk}/change/">{course.name}</a>')

    fieldsets = (
        ('Initials', {
            'fields': ('first_name', 'last_name', 'birthdate', 'course')
        }),
        ('Contacts', {
            'fields': ('email', 'phone_number')
        }),
        ('Media', {
            'classes': ('collapse',),
            'fields': ('avatar', 'resume')
        })
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
