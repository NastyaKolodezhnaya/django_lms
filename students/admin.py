from django.contrib import admin

from .models import Student, Course, Room, Color


# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Color)
