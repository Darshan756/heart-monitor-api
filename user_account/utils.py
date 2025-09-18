from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage


def send_link(request,user,subject,template):
    current_site = get_current_site(request)
    mail_subject = subject
    print(user.pk) 
    message = render_to_string(template,{
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    to_email = user.email
    send_mail = EmailMessage(mail_subject,message,to=[to_email])
    send_mail.send()
    