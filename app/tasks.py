from celery import task
from sendgrid import Mail
from app import sg
from app import app
from app import controllers
from flask import render_template


def app_context_task(run_func):
    @task
    def task_wrapper(*args, **kwargs):
        with app.app_context():
            return run_func(*args, **kwargs)

    return task_wrapper


@app_context_task
def send_sample_email():
    send_to = "prashant.khanduri@gmail.com"
    send_from = "prashant.khanduri@gmail.com"
    subject = "Sending with SendGrid is Fun"
    body = "and easy to do anywhere, even with Python"

    _send_message_with_sg(send_to, send_from, subject, body)


@app_context_task
def send_email_verification_link(user_xid):

    user = controllers.UserController.fetch_user(user_xid)
    send_to = user.email
    send_from = "prashant.khanduri@gmail.com"
    subject = "[Pulsico] Please verify your email!"

    link_data = {
        'user_xid': user_xid,
        'verification_token': user.email_verification_token,
    }
    body = render_template("email/email_verification.html", link_data=link_data)
    _send_message_with_sg(send_to, send_from, subject, body)


def _send_message_with_sg(send_to, send_from, subject, body):

    message = Mail()
    message.add_to(send_to)
    message.set_from(send_from)
    message.set_subject(subject)
    message.set_html(body)

    print "Sending email:({}) to :({})".format(subject, send_to)
    sg.send(message)
