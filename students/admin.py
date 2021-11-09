from django.contrib import admin

from courses.models import Course
from students.models import Profile

admin.site.register(Profile)
admin.site.register(Course)
