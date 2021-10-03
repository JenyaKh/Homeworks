from django.http import HttpResponse
import faker
from students.models import Student
from utils import format_records


def hello(request):
    return HttpResponse('SUCCESS')


def generate_students(request, count=10):
    fake = faker.Faker('ru_RU')
    while count > 0:
        new_student = Student(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email())
        new_student.save()
        count -= 1
    return HttpResponse('SUCCESS')


def get_students(request):
    students = Student.objects.all()
    result = format_records(students)
    return HttpResponse(result)
