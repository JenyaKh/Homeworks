from django.urls import path

from students.services.emails import password_reset_request
from students.views import StudentDelete, StudentList, StudentSearchList, \
    RegistrationStudent, UserLogin, LogoutStudent, ActivateUser, ActivateSentEmail, StudentProfile, StudentUpdate

app_name = 'students'

urlpatterns = [
    path('list/<str:type>', StudentList.as_view(), name='list-type'),
    path('list/', StudentList.as_view(), name='list'),
    path('update/<int:pk>/', StudentUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', StudentDelete.as_view(), name='delete'),
    path('search/', StudentSearchList.as_view(), name='search'),
    path('registration/', RegistrationStudent.as_view(), name='registration'),
    path('login/', UserLogin.as_view(), name='login'),
    path("logout/", LogoutStudent.as_view(), name="logout"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('activate/<str:uidb64>/<str:token>', ActivateUser.as_view(),
         name='activate'),
    path('activate/sent', ActivateSentEmail.as_view(), name='sent-email'),
    path('profile/<int:pk>/', StudentProfile.as_view(), name='profile'),

]
