def format_records(records):  # formatting list of values into string
    if not records:
        return 'Empty recordset('
    return '<br>'.join([str(rec) for rec in records])