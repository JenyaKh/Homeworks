from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from courses.models import Course
from students.models import Profile, CustomUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['type', 'last_name', 'first_name', 'phone_number', 'course_count', 'list_courses', 'view_user']
    ordering = ['type', 'last_name']
    search_fields = ['last_name__startswith']
    list_filter = ['type']
    fieldsets = [('Education', {'fields': ('type', 'course')}),
                 ('Personal info', {'fields': ('last_name', 'first_name', 'birthdate')}),
                 ('Contacts', {'fields': ('phone_number',)}),
                 ('Other', {'fields': ('avatar', 'resume')})]

    def view_user(self, obj):
        user = CustomUser.objects.get(id=obj.user_id)
        link = f"<a href='{reverse('admin:students_customuser_change', args={user.id})}'>{user.email}</a>"

        return format_html(link)

    def course_count(self, obj):
        if obj.course:
            courses = obj.course.all().count()
            return format_html(f"<p>{courses}</p>")
        else:
            return format_html("<p>0</p>")

    def list_courses(self, obj):
        if obj.course:
            courses = obj.course.all()
            links = [
                f"<a href='{reverse('admin:courses_course_change',args={course.id})}'>{course.name}</a></p>"
                for course in courses]

            return format_html(f"{''.join(links)}")
        else:
            return format_html("Empty courses")


class ViewProfileAdmin(admin.TabularInline):
    model = Profile.course.through
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'students_count', 'teachers_count']
    ordering = ['name']
    search_fields = ['name__icontains']
    inlines = [ViewProfileAdmin]

    def students_count(self, obj):
        students = Profile.objects.filter(course=obj.id).filter(type='student').count()
        return format_html(f"<p>{students}</p>")

    def teachers_count(self, obj):
        teachers = Profile.objects.filter(course=obj.id).filter(type='teacher').count()
        return format_html(f"<p>{teachers}</p>")


class ViewProfileAdmin(admin.StackedInline):
    model = Profile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_joined', 'is_active', 'view_profile']
    list_filter = ['is_active', 'is_staff']
    ordering = ['date_joined']
    search_fields = ['email__icontains']
    inlines = [ViewProfileAdmin]

    def view_profile(self, obj):
        user_prof = Profile.objects.get(user=obj.id)
        link = f"<a href='{reverse('admin:students_profile_change', args={user_prof.id})}'>{user_prof.full_name()}</a>"

        return format_html(link)
