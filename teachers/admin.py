from django.contrib import admin
from django.utils.html import format_html

from .models import Teacher

URL_COURSES = 'http://127.0.0.1:8000/admin/courses/course/'


# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'course_list']
    ordering = ['email']

    def course_list(self, obj):
        if obj.course:
            courses = obj.course.all()
            links = [f"<a href='{URL_COURSES}"
                     f"{course.pk}/change/'>{course.name}</p>"
                     for course in courses]
            return format_html(f"{''.join(links)}")
        else:
            return ''
