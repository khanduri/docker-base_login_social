fake_verify_link_data = {'link_data': {'user_xid': 'fake_xid',
                                       'verification_token': 'FAKE_LINK_TOKEN',
                                       '_external': True}}
EMAIL_TEMPLATE_MAP = {
    'email_verify': ("email/email_verification.html", fake_verify_link_data),
}