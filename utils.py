def format_records(records, app):
    if not records:
        return '(Empty recordset)'
    return '<br>'.join(f'<a href="/{app}/update/{rec.id}/">EDIT</a> {rec}'
                       for rec in records)
