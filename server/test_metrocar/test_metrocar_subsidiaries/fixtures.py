from metrocar.subsidiaries.models import Subsidiary

def get_subsidiary():
    return Subsidiary.objects.get_current()