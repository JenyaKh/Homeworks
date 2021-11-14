import datetime

from django.contrib.auth.models import User
from django.core import validators
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor')
    ]
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    phone_number = PhoneNumberField(unique=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    budget = models.BooleanField(null=True)
    scholarship = models.BooleanField(null=True)
    resume = models.FileField(upload_to='documents/', null=True, blank=True,
                              validators=[validators.FileExtensionValidator(['txt', 'pdf', 'docx'],
                                                                            message='file must be txt, docx, pdf')])
    course = models.ForeignKey("courses.Course",
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    invited = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.full_name()} ({self.id})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def age(self):
        age = datetime.datetime.now().year - self.birthdate.year
        return age


class Invitations(models.Model):
    student = models.ForeignKey("students.Profile", null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120, null=False)
    invite_code = models.CharField(max_length=120, null=False)
    accept = models.BooleanField(null=True)
