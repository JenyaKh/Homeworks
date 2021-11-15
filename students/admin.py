from django.contrib import admin

from courses.models import Course
from students.models import Profile, CustomUser


admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(CustomUser)
