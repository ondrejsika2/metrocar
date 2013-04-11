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
            create_mail_template('INV_CS', 'INV_CS', 'Autonapůl - Faktura', 'Dobrý den, zasílá me Vám fakturaci za služby.',settings.LANG_CHOICES[0][0]),
            create_mail_template('INV_EN', 'INV_EN', 'Autonapůl - Invoice', 'Hello, we are sending you invoice.',settings.LANG_CHOICES[1][0]),
            create_mail_template('TAR_CS', 'TAR_CS', 'Autonapůl - Upozornění', 'Dobrý den, Váš účet vykazuje záporný zůstatek. Vyrovnejte si prosím stav Vašeho účtu. ',settings.LANG_CHOICES[0][0]),
            create_mail_template('TAR_EN', 'TAR_EN', 'Autonapůl - Warning', 'Hello, your account has negative balance. Please refund your liability. ',settings.LANG_CHOICES[1][0]),
        ],
    }