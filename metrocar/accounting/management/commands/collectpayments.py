from django.core.management.base import NoArgsCommand
from django.utils import importlib
from metrocar.utils.log import get_logger
from django.conf import settings


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
    	"""
    	This command should be automaticly executed by cron for example every hour
    	or at least once a day.
    	"""
        if settings.ACCOUNTING_ENABLED:
            try:
                accounting = importlib.import_module(settings.ACCOUNTING['IMPLEMENTATION'])
                account_instance = accounting.get_accounting_instance()
                account_instance.check_incoming_payments()		        
            except ImportError, ex:
                get_logger().error("Can't import accounting implementation from settings")   
