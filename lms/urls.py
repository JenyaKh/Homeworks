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
from django.urls import path, include

from lms import settings
from students.views import hello, generate_students, index
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="index"),
    path("index/", index),
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('generate_students/', generate_students),
    path('generate_students/count=<int:count>/', generate_students),
    path('students/', include('students.urls')),

]

handler404 = 'students.views.page_not_found_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
