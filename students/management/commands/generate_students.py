from django.core.management.base import BaseCommand
from faker import Faker
from students.models import Student


class Command(BaseCommand):
    help = u'creating random students'

    def add_arguments(self, parser):
        parser.add_argument('count', default=10, type=int, help=u'number of students', nargs='?')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        faker = Faker()
        for i in range(count):
            st = Student(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y", end_date="-18y")
            )
            st.save()
