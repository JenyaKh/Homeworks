from django.db import models
import datetime


# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=80, null=False)
    faculty = models.CharField(max_length=80, null=False)
    handler = models.EmailField(max_length=120, null=True)
    start_year = models.CharField(max_length=4, null=True, default=datetime.datetime.now().year)
