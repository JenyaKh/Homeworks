import datetime

from django.forms import ModelForm
from django.core.validators import ValidationError
from students.models import Student, Teacher


class PersonBaseForm(ModelForm):
    class Meta:
        abstract = True
    fields = ['first_name', 'last_name', 'email', 'phone_number']

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        return self.normalize_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        return self.normalize_name(last_name)

    def clean(self):
        cleaned_data = super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if first_name == last_name:
            raise ValidationError('ERROR: First and last names can\'t be equal')

        return cleaned_data

    def clean_email(self):
        DOMAIN_LIST = ['@yandex.ru', '@yandex.com', '@yandex.ua', '@ya.ru', '@ya.com',
                       '@mail.ru', '@mail.ua', '@inbox.ru', '@list.ru', '@bk.ru', '@rambler.ru']
        email = self.cleaned_data['email']
        for domain in DOMAIN_LIST:
            if domain in email.lower():
                raise ValidationError(f'ERROR: it is forbidden to use the domain {domain}')

        return email


class StudentCreateForm(PersonBaseForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'birthdate', 'phone_number', 'budget', 'scholarship', 'course']

    def clean_birthdate(self):
        min_age = 18
        birthdate = self.cleaned_data['birthdate']
        if datetime.date.today().year - birthdate.year < min_age:
            raise ValidationError('ERROR: the student must be at least 18 years old')

        return birthdate

    def clean(self):
        cleaned_data = super().clean()

        budget = self.cleaned_data['budget']
        scholarship = self.cleaned_data['scholarship']
        if not budget and scholarship:
            raise ValidationError('ERROR: student can receive a scholarship only on a budget')

        return cleaned_data


class StudentUpdateForm(PersonBaseForm):
    class Meta(PersonBaseForm.Meta):
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'budget', 'scholarship', 'course']


class TeacherCreateForm(PersonBaseForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone_number", "course"]
