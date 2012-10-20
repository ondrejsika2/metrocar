from datetime import datetime


def entry(**kwargs):
    defaults = dict(
        unit_id=321,
        timestamp=datetime(2012, 12, 12, 12, 12, 12),
        location=(10, 20),
        added=datetime(2012, 12, 12, 12, 12, 13),
        custom_field=42,
    )
    return dict(defaults, **kwargs)
