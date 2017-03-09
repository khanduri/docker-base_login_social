from app import app
from flask import request
from flask.ext.login import login_required
import tasks
from app.helpers import api_response


@app.route('/api/v1/users/<user_xid>/resend_verify', methods=['POST'])
@login_required
def resend_verification(user_xid):
    if request.method == 'POST':
        if not api_response.validate_user(user_xid):
            return api_response.return_packet_invalid_user()

        tasks.send_email_verification_link.apply_async((user_xid, ))
        return api_response.return_packet_success()

    return api_response.return_packet_not_supported()
