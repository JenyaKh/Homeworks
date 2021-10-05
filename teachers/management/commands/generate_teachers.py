from django.core.management.base import BaseCommand
from teachers.models import Teacher


class Command(BaseCommand):
    help = u'creating random teachers'

    def add_arguments(self, parser):
        parser.add_argument('count', default=10, type=int, help=u'number of teachers', nargs='?')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        Teacher.generate_teachers(count)
