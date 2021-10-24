import datetime
import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from faker import Faker
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):

    # id = models.UUIDField(primary_key=True, unique=True,
    #                       default=uuid.uuid4,
    #                       editable=False)

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

    birthdate = models.DateField(null=True, default=datetime.date.today)
    budget = models.BooleanField(null=True)
    scholarship = models.BooleanField(null=True)
    course = models.ForeignKey("students.Course",
                               null=True,
                               on_delete=models.SET_NULL)

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


class Course(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(null=False, max_length=100)
    start_date = models.DateField(null=True, default=datetime.date.today())
    count_of_students = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Teacher(Person):
    course = models.ManyToManyField(to="students.Course")

    def __str__(self):
        return f"{self.email} ({self.id})"
