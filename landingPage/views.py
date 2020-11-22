from django.shortcuts import render
import os

import smtplib
import ssl
import email
from email.mime.text import MIMEText

# Create your views here.

def createEmailBody(name, user_email, body_text):
    body_mail = """
        <html>\
            <body>
                <span style="font-weight: bold">NOMBRES: </span><span>%s</span> <br />
                <span style="font-weight: bold">EMAIL: </span><span>%s</span> <br />                
                <span style="font-weight: bold">MENSAJE: </span><span>%s</span> <br />                
            </body>
        </html>""" % (name, user_email, body_text)
    return body_mail


def sendEmail(body_mail, subject):
    try:
        from django.core.mail import send_mail
        from django.conf import settings

        send_mail(
            "Formulario de contactenos",
            "",
            settings.EMAIL_HOST_USER,
            ['info.liciorion@gmail.com'],
            fail_silently=False,
            html_message=body_mail,
        )

        return True

    except:
        return False



def landingView(request):
    return render(request, 'index.html')


def contactView(request):
    if request.method == "POST":
        name = request.POST['full_name']
        user_email = request.POST['email']
        message = request.POST['message']
        subject = request.POST['subject']
        # Build email body
        body_message = createEmailBody(name, user_email, message)
        # Send email
        sendEmail(body_message, subject)

        return render(request, 'contact_me_done.html')

    else:
        return render(request, 'contact.html')


def welcomeView(request):
    return render(request, 'welcome.html')
