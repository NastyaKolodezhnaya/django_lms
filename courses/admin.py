from django.contrib import admin
from django.utils.html import format_html

from .models import Course
from students.models import Student


URL_STUDENTS = 'http://127.0.0.1:8000/admin/students/student'


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
                f'<a href="{URL_STUDENTS}/?course__id__exact{instance.id}/">'
                f'{instance.count_of_students}</a>'
            )
