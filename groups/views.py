from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from groups.forms import GroupCreateForm
from groups.models import Group
from utils import format_records


def get_groups(request):

    groups = Group.objects.all()

    result = format_records(groups)

    return HttpResponse(result)


@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/groups')

    elif request.method == 'GET':
        form = GroupCreateForm()

    form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

    return HttpResponse(form_html)
