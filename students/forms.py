import datetime

from django.forms import ModelForm
from django.core.validators import ValidationError
from students.models import Student


class StudentBaseForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'birthdate', 'phone_number']

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
        domain_list = ['@yandex.ru', '@yandex.com', '@yandex.ua', '@ya.ru', '@ya.com',
                       '@mail.ru', '@mail.ua', '@inbox.ru', '@list.ru', '@bk.ru', '@rambler.ru']
        email = self.cleaned_data['email']
        for domain in domain_list:
            if domain in email:
                raise ValidationError(f'ERROR: it is forbidden to use the domain {domain}')

        return email

    def clean_birthdate(self):

        min_age = 18
        birthdate = self.cleaned_data['birthdate']
        if datetime.date.today().year - birthdate.year < min_age:
            raise ValidationError('ERROR: the student must be at least 18 years old')

        return birthdate


class StudentCreateForm(StudentBaseForm):
    pass


class StudentUpdateForm(StudentBaseForm):
    class Meta(StudentBaseForm.Meta):
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthdate']
