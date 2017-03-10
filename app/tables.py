from flask.ext.login import UserMixin
from hashlib import md5
from app import (
    db,
    lm,
    hashids,
)
from sqlalchemy import func
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)
import uuid


Base = declarative_base()


class BaseDBMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, server_default=func.now())
    removed_at = db.Column(db.TIMESTAMP)
    # updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    @property
    def xid(self):
        return hashids.encode(self.id)

    @classmethod
    def id_from_xid(cls, xid):
        decoded_value = hashids.decode(xid)
        return decoded_value[0] if decoded_value else None


class User(db.Model, UserMixin, BaseDBMixin):

    __tablename__ = 'User'

    email = db.Column(db.String(255), nullable=True)
    last_seen = db.Column(db.DateTime)
    nickname = db.Column(db.String(63), nullable=False)
    about_me = db.Column(db.String(1023))
    timezone = db.Column(db.String(255))
    email_verification_token = db.Column(db.String(1023), default=uuid.uuid4().hex)

    __table_args__ = (
        UniqueConstraint('email', 'email_verification_token', 'removed_at'),
    )

    @property
    def email_verified(self):
        return self.email_verification_token is None

    def __repr__(self):
        return '<User xid:{} - nickname:{}>'.format(self.xid, self.nickname)

    def is_admin(self):
        return self.id == 1

    def avatar(self, size):
        md_hash = md5(self.email.encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md_hash, size)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserSocial(db.Model, BaseDBMixin):

    __tablename__ = 'UserSocial'

    user_id = db.Column(db.Integer)
    user = db.relationship(
        'User',
        primaryjoin='User.id == UserSocial.user_id',
        foreign_keys='UserSocial.user_id',
    )

    social_network = db.Column(db.String(63), nullable=False)
    social_id = db.Column(db.String(255), nullable=False)
    access_code = db.Column(db.String(2047))

    __table_args__ = (
        UniqueConstraint('social_network', 'social_id', 'removed_at'),
    )


class Contact(db.Model, BaseDBMixin):

    __tablename__ = 'Contact'

    user_id = db.Column(db.Integer, nullable=True)
    user = db.relationship(
        'User',
        primaryjoin='User.id == Contact.user_id',
        foreign_keys='Contact.user_id',
    )

    email = db.Column(db.String(63), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    message = db.Column(db.String(1023))

