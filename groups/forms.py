from django.forms import ModelForm
from groups.models import Group


class GroupBaseForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'faculty', 'handler', 'start_year']


class GroupCreateForm(GroupBaseForm):
    pass


class GroupUpdateForm(GroupBaseForm):
    class Meta(GroupBaseForm.Meta):
        fields = ['name', 'faculty', 'handler', 'start_year']

