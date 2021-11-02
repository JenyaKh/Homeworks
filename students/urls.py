from django.urls import path

from students.views import StudentCreate, StudentUpdate, StudentDelete, StudentList, StudentSearchList, \
    RegistrationStudent, UserLogin, LogoutStudent, send_email, password_reset_request

app_name = 'students'

urlpatterns = [
    path('', StudentList.as_view(), name='list'),
    path('create/', StudentCreate.as_view(), name='create'),
    path('update/<int:pk>/', StudentUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', StudentDelete.as_view(), name='delete'),
    path('search/', StudentSearchList.as_view(), name='search'),
    path('registration/', RegistrationStudent.as_view(), name='registration'),
    path('login/', UserLogin.as_view(), name='login'),
    path("logout/", LogoutStudent.as_view(), name="logout"),
    path('send_email/', send_email, name='send_email'),
    path("password_reset/", password_reset_request, name="password_reset")
]
