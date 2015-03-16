# encoding: utf-8

from django.conf import settings
from metrocar.utils.models import EmailTemplate

def create_mail_template(code, name, subject, content, language):
	return EmailTemplate.objects.get_or_create(
    	code=code,
    	name=name,
    	subject=subject,
    	content=content,
    	language=language)[0]	

def create():
    return {
        'emailtemplates': [
            create_mail_template('INV_CS', 'INV_CS', 'Autonapůl - Faktura', 'Dobrý den, zasílá me Vám fakturaci za služby. Tuto fakturu neplaťte, částka bla již uhrazena z Vašeho konta v systému.',settings.LANG_CHOICES[0][0]),
            create_mail_template('INV_EN', 'INV_EN', 'Autonapůl - Invoice', 'Hello, we are sending you invoice. Do NOT PAY this invoice. Money were already taken from your system account.' ,settings.LANG_CHOICES[1][0]),
            create_mail_template('INV_A_CS', 'INV_ACTIVE_CS', 'Autonapůl - Faktura', 'Dobrý den, zasílá me Vám fakturaci za služby. Tuto fakturu je třeba uhradit do data splatnosti uvedeného ve faktuře.',settings.LANG_CHOICES[0][0]),
            create_mail_template('INV_A_EN', 'INV_ACTIVE_EN', 'Autonapůl - Invoice', 'Hello, we are sending you invoice. Please transfer money for this invoice to our account before due date.' ,settings.LANG_CHOICES[1][0]),
            create_mail_template('TAR_CS', 'TAR_CS', 'Autonapůl - Upozornění', 'Dobrý den, Váš účet vykazuje záporný zůstatek. Vyrovnejte si prosím stav Vašeho účtu. ',settings.LANG_CHOICES[0][0]),
            create_mail_template('TAR_EN', 'TAR_EN', 'Autonapůl - Warning', 'Hello, your account has negative balance. Please refund your liability. ',settings.LANG_CHOICES[1][0]),
        ],
    }