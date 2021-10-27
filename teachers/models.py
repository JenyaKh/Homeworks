from django.db import models

from students.models import Person


class Teacher(Person):
    course = models.ManyToManyField(to="courses.Course")

    def __str__(self):
        return f"{self.email} ({self.id})"
