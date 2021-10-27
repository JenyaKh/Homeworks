from students.forms import PersonBaseForm
from teachers.models import Teacher


class TeacherCreateForm(PersonBaseForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone_number", "course"]
