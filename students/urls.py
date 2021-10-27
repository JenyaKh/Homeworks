from django.urls import path

from students.views import StudentCreate, StudentUpdate, StudentDelete, StudentList, StudentSearchList

app_name = 'students'

urlpatterns = [
    path('', StudentList.as_view(), name='list'),
    path('create/', StudentCreate.as_view(), name='create'),
    path('update/<int:pk>/', StudentUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', StudentDelete.as_view(), name='delete'),
    path('search/', StudentSearchList.as_view(), name='search'),
]
