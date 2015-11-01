from celery import task
from sendgrid import Mail
from app import sg


@task
def send_sample_email():

    message = Mail()
    message.add_to("prashant.khanduri@gmail.com")
    message.set_from("prashant.khanduri@gmail.com")
    message.set_subject("Sending with SendGrid is Fun")
    message.set_html("and easy to do anywhere, even with Python")
    sg.send(message)

    print "Sending email"
