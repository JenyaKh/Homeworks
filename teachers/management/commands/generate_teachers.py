import faker
from django.core.management.base import BaseCommand
from teachers.models import Teacher


class Command(BaseCommand):
    help = u'creating random teachers'

    def add_arguments(self, parser):
        parser.add_argument('count', default=10, type=int, help=u'number of teachers', nargs='?')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = faker.Faker('ru_RU')
        while count > 0:
            new_teacher = Teacher(first_name=fake.first_name(), last_name=fake.last_name(), faculty='IT')
            new_teacher.save()
            count -= 1
