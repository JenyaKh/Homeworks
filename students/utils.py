from django.urls import reverse


def format_records(records):
    if not records:
        return '(Empty recordset)'
    return '<br>'.join(f'<a href="{reverse("students:update", args=(rec.id,))}">EDIT </a>'
                       f'<a href="{reverse("students:delete", args=(rec.id,))}">DELETE </a> {rec}' for rec in records)
