from app.tasks.emails import base
from app import celery


@celery.task()
def send_sample_email():
    send_to = "prashant.khanduri@gmail.com"
    send_from = "prashant.khanduri@gmail.com"
    subject = "Sending with SendGrid is Fun"
    body = "and easy to do anywhere, even with Python"

    base.send_message_with_sg(send_to, send_from, subject, body)
