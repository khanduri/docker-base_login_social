from app import app
from flask import request
from flask import g
import tables
from flask import jsonify
from flask.ext.login import login_required
import tasks


def _pack_response(data, meta=None):
    packed_data = {
        'data': data,
        'meta': meta
    }
    return jsonify(packed_data)


def _validate_user(user_xid):
    user = g.user if g.user.is_authenticated else None
    request_user_id = tables.User.id_from_xid(user_xid)
    return user.id == request_user_id


def _return_packet_invalid_user():
    response = {
        'success': False,
        'code': 'user_mismatch',
        'message': "Sorry! We're unable to process that request for you.",
    }
    return _pack_response(response)


def _return_packet_invalid_form():
    response = {
        'success': False,
        'code': 'invalid_form',
        'message': 'The reminder form had invalid values',
    }
    return _pack_response(response)


def _return_packet_not_supported():
    response = {
        'success': False,
        'code': 'not-supported',
        'message': "Sorry! We're unable to process that request for you.",
    }
    return _pack_response(response)


def _return_packet_success(data=None):
    response = {'success': True, }
    if data:
        response.update(data)
    return _pack_response(response)


@app.route('/api/v1/users/<user_xid>/resend_verify', methods=['POST'])
@login_required
def resend_verification(user_xid):
    if request.method == 'POST':
        if not _validate_user(user_xid):
            return _return_packet_invalid_user()

        tasks.send_email_verification_link.apply_async((user_xid, ))
        return _return_packet_success()

    return _return_packet_not_supported()

