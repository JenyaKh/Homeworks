from django.urls import reverse


def format_records(records, path_name):
    if not records:
        return '(Empty recordset)'
    return '<br>'.join(f'<a href="{reverse(path_name, args=(rec.id,))}">EDIT</a> {rec}' for rec in records)

