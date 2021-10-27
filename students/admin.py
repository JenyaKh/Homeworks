from django.contrib import admin

from courses.models import Course
from teachers.models import Teacher
from .models import Student

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Teacher)
