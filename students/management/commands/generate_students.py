from django.core.management.base import BaseCommand
from students.models import Student


class Command(BaseCommand):
    help = u'creating random students'

    def add_arguments(self, parser):
        parser.add_argument('count', default=10, type=int, help=u'number of students', nargs='?')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        Student.generate_instances(count)
