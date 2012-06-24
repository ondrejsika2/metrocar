from metrocar.settings.base import *

try:
    from metrocar.settings.local import *
except ImportError:
    pass
