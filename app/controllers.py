from app import tables
from app import db
import uuid


class UserController(object):

    @classmethod
    def id_from_xid(cls, user_xid):
        return tables.User.id_from_xid(user_xid)

    @classmethod
    def fetch_all_users(cls, user_ids):
        users = tables.User.query.filter(tables.User.id.in_(user_ids))
        return users

    @classmethod
    def fetch_user_with_nickname(cls, nickname):
        return tables.User.query.filter_by(nickname=nickname).first()

    @classmethod
    def create_or_update_user(cls, social_id, social_network, access_code, email, username):

        user_social = tables.UserSocial.query.filter_by(social_id=social_id).first()
        if not user_social:
            user = tables.User(nickname=username, email=email)
            user_social = tables.UserSocial(social_network=social_network,
                                            social_id=social_id,
                                            access_code=access_code)
            user_social.user = user

            db.session.add(user)
            db.session.add(user_social)

        else:
            user = tables.User.query.filter_by(id=user_social.user_id).first()

            user_social.access_code = access_code
            db.session.add(user_social)

        db.session.commit()

        return user

    @classmethod
    def update_user_profile(cls, user_xid, nickname, email, timezone, about_me):

        user = cls.fetch_user(user_xid)
        user.nickname = nickname
        user.timezone = timezone
        user.about_me = about_me

        if user.email != email:
            user.email = email
            user.email_verification_token = uuid.uuid4().hex

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def update_user_email_verification(cls, user_xid, verification_token):
        user = cls.fetch_user(user_xid)

        if user.email_verification_token == verification_token:
            user.email_verification_token = None
            db.session.add(user)
            db.session.commit()

        return user

    @classmethod
    def fetch_user(cls, user_xid):
        user_id = tables.User.id_from_xid(user_xid)
        user = tables.User.query \
            .filter(
                tables.User.id == user_id,
                tables.User.removed_at.is_(None)) \
            .first()
        return user

    @classmethod
    def create_user_and_social_details(cls, username, email, social_network, social_id, access_code):
        pass


class UserSocialController(object):

    @classmethod
    def fetch_user_social(cls, social_id):
        return tables.UserSocial.query.filter_by(social_id=social_id).first()


class ContactController(object):

    @classmethod
    def create_contact(cls, message, email=None, name=None, user=None):
        contact = tables.Contact()

        contact.message = message
        contact.email = email
        contact.name = name

        if user:
            contact.user = user

        db.session.add(contact)
        db.session.commit()

        return contact
