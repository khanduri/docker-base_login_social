from app import app
from flask import request
from flask_login import login_required
from app.helpers import api_response
from app.tasks.emails.verification_email import send_email_verification_link


@app.route('/api/v1/users/<user_xid>/resend_verify', methods=['POST'])
@login_required
def resend_verification(user_xid):
    if request.method == 'POST':
        if not api_response.validate_user(user_xid):
            return api_response.return_packet_invalid_user()

        send_email_verification_link.apply_async((user_xid, ))
        return api_response.return_packet_success()

    return api_response.return_packet_not_supported()
