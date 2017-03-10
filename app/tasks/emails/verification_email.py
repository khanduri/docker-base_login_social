from app import controllers
from app.tasks.base import app_context_task
from app.tasks.emails import base
from flask import render_template


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
    base.send_message_with_sg(send_to, send_from, subject, body)
