'''
Created on 5.3.2010

@author: xaralis
'''
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Model
import sys
from metrocar.utils.log import get_logger
from metrocar.utils.models import EmailTemplate

class EmailSender:
    @classmethod
    def send_mail(cls, recipients, template_code, template_lang, params, params2={}, attachment_path=None):
        """
        Generic wrapper for saving e-mails with
        """
        et = EmailTemplate.objects.get(code=template_code, language=template_lang)

        if isinstance(params, Model):
            # if object instance, convert to the dict
            from metrocar.utils.serializers import to_dict
            params = to_dict(params)
	
	#params is list of dict, we need only dict so !! TODO CRITICAL can something be at higher indexes??
	params = params[0]
	assert isinstance(params, dict)

        params.update(params2)
        
        subject = et.render_subject( ** params)
        message = et.render_content( ** params)

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipients)
        if(attachment_path != None):
            email.attach_file(attachment_path)
		
        try:
            email.send(fail_silently=False)
            get_logger().info("Mail " + template_code + "_" + template_lang + " sent to " + str(recipients))
        except Exception as ex:
            get_logger().error("Mail " + template_code + "_" + template_lang + " could not be sent. Exception was: " + str(ex))
