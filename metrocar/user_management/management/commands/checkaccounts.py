from django.core.management.base import NoArgsCommand
from metrocar.user_management.models import MetrocarUser, Account


class Command(NoArgsCommand):
	"""
	Runs every day and check state of accounts of all users.
	If account's balance is negative, the mail is send to the user.
	TODO: there should be some fee for having a negative balance.

	"""

	def handle_noargs(self, **options):
		for a in Account.objects.all():
			if a.balance < 0:
				a.send_warning_mail()

