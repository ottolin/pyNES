def get_class( class_name_string ):
    parts = class_name_string.split('.')
    module = ".".join(parts[:-1])
    rv = __import__( module )
    for components in parts[1:]:
        rv = getattr(rv, components)
    return rv