from app import tables
from app import controllers
from app import sg
from app import db
from app import app
import datetime
import collections
import pytz
from flask import render_template
from sendgrid import Mail


def send_email(send_to, title, body):
    message = Mail()
    message.add_to(send_to)
    message.set_from("prashant.khanduri@gmail.com")
    message.set_subject(title)
    message.set_html(body)
    sg.send(message)

    print "Sending to: {}".format(send_to)


def cron_reminder_triggers():

    now = datetime.datetime.now()
    today_date = datetime.datetime.today().date()

    reminders = tables.Reminder.query.filter(
        tables.Reminder.remind_date == today_date,
        tables.Reminder.triggered.is_(False),
    ).all()

    user_reminders = collections.defaultdict(list)
    for reminder in reminders:
        user_reminders[reminder.creator_id].append(reminder)

    user_ids = user_reminders.keys()
    if not user_ids:
        print "No users to send reminders to."
        return

    users = controllers.UserController.fetch_all_users(user_ids)

    for user in users:
        if not user.email:
        # if not user.email or not user.email_verified:
            continue

        user_timezone_dt = to_local_time(now, user.timezone or 'US/Pacific')
        if today_date != user_timezone_dt.date():
            continue
        reminders = user_reminders[user.id]
        send_user_reminder(user, reminders)


def send_user_reminder(user, reminders):

    email_body = render_template("email/template_reminder_notice.html", reminders=reminders)
    email_title = "[Pulsico] Remember today you have to ..."
    send_to = user.email

    for reminder in reminders:
        reminder.triggered = True
        db.session.add(reminder)

    send_email(send_to, email_title, email_body)
    db.session.commit()


def to_local_time(dt, tz_str):
    return dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(tz_str))


if __name__ == '__main__':
    with app.app_context():
        cron_reminder_triggers()
