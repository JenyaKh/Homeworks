from django.db import models

# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    faculty = models.CharField(max_length=80, null=False)
    phone = models.CharField(max_length=80, null=True)
    birthdate = models.DateField(null=True)
