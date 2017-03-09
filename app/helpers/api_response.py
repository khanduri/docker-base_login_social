from flask import g
from flask import jsonify

from app import tables


def _pack_response(data, meta=None):
    packed_data = {
        'data': data,
        'meta': meta
    }
    return jsonify(packed_data)


def validate_user(user_xid):
    user = g.user if g.user.is_authenticated else None
    request_user_id = tables.User.id_from_xid(user_xid)
    return user.id == request_user_id


def return_packet_invalid_user():
    response = {
        'success': False,
        'code': 'user_mismatch',
        'message': "Sorry! We're unable to process that request for you.",
    }
    return _pack_response(response)


def return_packet_invalid_form():
    response = {
        'success': False,
        'code': 'invalid_form',
        'message': 'The reminder form had invalid values',
    }
    return _pack_response(response)


def return_packet_not_supported():
    response = {
        'success': False,
        'code': 'not-supported',
        'message': "Sorry! We're unable to process that request for you.",
    }
    return _pack_response(response)


def return_packet_success(data=None):
    response = {'success': True}
    if data:
        response.update(data)
    return _pack_response(response)
