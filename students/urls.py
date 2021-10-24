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

from django.urls import path

from students.views import (get_students, create_student, update_student,
                            delete_student, create_teacher, get_teachers)

app_name = 'students'

urlpatterns = [
    path('', get_students, {'selected_id': "all"}, name='list'),
    path('create/', create_student, name='create'),
    path('update/<int:pk>/', update_student, name='update'),
    path('delete/<int:pk>/', delete_student, name='delete'),
    path("create-teacher/", create_teacher, name="create-teacher"),
    path("list-teachers/", get_teachers, {'selected_id': "all"}, name='list-teachers'),
    path('search/', get_students, name='search'),
    path('search-by-course/student', get_students,  name='search-by-course-student'),
    path('search-by-course/teacher', get_teachers,  name='search-by-course-teacher'),
]
