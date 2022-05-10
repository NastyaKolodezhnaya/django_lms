from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode

from .models import Course
from students.models import Student


# Register your models here.
class StudentInline(admin.StackedInline):
    model = Student
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'students_count']
    ordering = ['name']
    search_fields = ['name']

    inlines = [StudentInline]

    def students_count(self, instance):
        if instance.count_of_students:
            return format_html(
                f'<a href="http://127.0.0.1:8000/admin/students/student/?course__id__exact{instance.id}/">{instance.count_of_students}</a>'
            )
