from django.urls import path
from teachers.views import TeacherCreate, TeacherList, TeacherSearchList

app_name = 'teachers'

urlpatterns = [
    path("create/", TeacherCreate.as_view(), name="create"),
    path("list/", TeacherList.as_view(), name='list'),
    path('search/', TeacherSearchList.as_view(),  name='search'),
]
