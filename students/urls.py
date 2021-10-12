"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from groups.views import create_group, get_groups
from students.views import hello, generate_students, get_students, create_student, update_student, delete_student
from teachers.views import get_teachers, create_teacher

urlpatterns = [

    path('', get_students, name='students-list'),
    path('create/', create_student, name='student-create'),
    path('update/<int:pk>/', update_student, name='student-update'),
    path('delete/<int:pk>/', delete_student, name='student-delete'),

]
