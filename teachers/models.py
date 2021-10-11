from django.db import models
from faker import Faker


class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    faculty = models.CharField(max_length=80, null=False)
    phone = models.CharField(max_length=80, null=True)
    birthdate = models.DateField(null=True)

    def __str__(self):
        return f'{self.full_name()} ({self.id})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def generate_teachers(cls, count):
        faker = Faker()
        for i in range(count):
            tch = Teacher(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                faculty=faker.job(),
                phone=faker.phone_number(),
                birthdate=faker.date_time_between(start_date="-80y", end_date="-22y")
            )
            tch.save()
