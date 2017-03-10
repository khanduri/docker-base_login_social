import time
from app import controllers


def create_user(social_id=None,
                social_network='temp_network',
                access_code='temp_access_code',
                email=None,
                username=None):

    now = int(round(time.time() * 1000))
    username = username if username else 'temp_user_%s' % now
    social_id = social_id if social_id else 'id_%s' % now
    email = email if email else 'temp_%s@email.com' % now

    user = controllers.UserController.create_or_update_user(social_id,
                                                            social_network,
                                                            access_code,
                                                            email,
                                                            username)

    return user
