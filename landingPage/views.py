from django.shortcuts import render
import os

import smtplib
import ssl
import email
from email.mime.multipart import MIMEMultipart
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
        # Connect to SMTP server provider
        email_server = smtplib.SMTP(os.environ.get(
            'EMAIL_HOST', None), os.environ.get('EMAIL_PORT', None))
        email_server.ehlo()
        email_server.starttls()
        email_server.ehlo()
        email_server.login(os.environ.get('EMAIL_HOST_USER', None),
                           os.environ.get('EMAIL_HOST_PASSWORD', None))
        # Build email structure
        msg = MIMEText(body_mail, 'html')
        msg['Subject'] = subject

        # Send email
        email_server.sendmail(os.environ.get('EMAIL_HOST_USER', None), os.environ.get('EMAIL_CONTACT_USER', None),
                              msg.as_string().encode("ascii", errors="ignore"))

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
