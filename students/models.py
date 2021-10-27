import datetime
from django.core import validators
from faker import Faker
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(max_length=120, null=True, unique=True)
    phone_number = PhoneNumberField(unique=True, null=True, )

    def __str__(self):
        return f'{self.full_name()} ({self.id})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        abstract = True


class Student(Person):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birthdate = models.DateField(null=True, default=datetime.date.today)
    budget = models.BooleanField(null=True)
    scholarship = models.BooleanField(null=True)
    resume = models.FileField(upload_to='documents/', null=True, blank=True,
                              validators=[validators.FileExtensionValidator(['txt', 'pdf', 'docx'],
                                                                            message='file must be txt, docx, pdf')])
    course = models.ForeignKey("courses.Course",
                               null=True,
                               on_delete=models.SET_NULL)
    invited = models.IntegerField(default=0, null=True)

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            st = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y", end_date="-18y"),
            )
            st.save()

    def age(self):
        return datetime.datetime.now().year - self.birthdate.year


class Invitations(models.Model):
    student = models.ForeignKey("students.Student", null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120, null=False)
    invite_code = models.CharField(max_length=120, null=False)
    accept = models.BooleanField(null=True)
