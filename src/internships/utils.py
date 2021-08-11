def convert_int_or_none(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None