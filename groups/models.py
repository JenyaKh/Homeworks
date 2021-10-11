from faker import Faker
from django.db import models

import datetime


class Group(models.Model):
    name = models.CharField(max_length=80, null=False)
    faculty = models.CharField(max_length=80, null=False)
    handler = models.CharField(max_length=100, null=True)
    start_year = models.CharField(max_length=4, null=True, default=datetime.datetime.now().year)

    def __str__(self):
        return f'{self.name} ({self.id})'

    @classmethod
    def generate_groups(cls, count):
        faker = Faker()
        for i in range(count):
            year = faker.year()
            gr = Group(
                name=faker.word() + year,
                faculty=faker.job(),
                handler=f'{faker.last_name()} {faker.first_name()}',
                start_year=year
            )
            gr.save()
