from sendgrid.helpers.mail import Mail
from app import sg


def send_message_with_sg(send_to, send_from, subject, body):

    message = Mail()
    message.add_to(send_to)
    message.set_from(send_from)
    message.set_subject(subject)
    message.set_html(body)

    print("Sending email:({}) to :({})".format(subject, send_to))
    sg.send(message)
