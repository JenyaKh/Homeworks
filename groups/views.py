from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from groups.forms import GroupCreateForm, GroupUpdateForm
from groups.models import Group
from groups.utils import format_records


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
            return HttpResponseRedirect(reverse('groups:list'))

    elif request.method == 'GET':
        form = GroupCreateForm()

    form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

    return HttpResponse(form_html)


@csrf_exempt
def update_group(request, pk):

    student = get_object_or_404(Group, id=pk)

    if request.method == 'POST':
        form = GroupCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('groups:list'))

    elif request.method == 'GET':
        form = GroupUpdateForm(instance=student)

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """

    return HttpResponse(form_html)
