from django.urls import reverse


def format_records(records):
    if not records:
        return '(Empty recordset)'
    return '<br>'.join(f'<a href="{reverse("teachers:update", args=(rec.id,))}">EDIT</a> {rec}' for rec in records)
