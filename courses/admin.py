from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode

from .models import Course, Room, Color
from students.models import Student


# Register your models here.
class StudentInline(admin.StackedInline):
    model = Student
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_of_students', 'room']
    ordering = ['name']
    search_fields = ['name', 'room']

    inlines = [StudentInline]


admin.site.register(Room)
admin.site.register(Color)
