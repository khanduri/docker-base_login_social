from flask.ext.login import UserMixin
from hashlib import md5
from app import (
    db,
    lm,
    hashids,
)
from sqlalchemy import func
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)


Base = declarative_base()


class BaseDBMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, server_default=func.now())
    # updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    @property
    def xid(self):
        return hashids.encode(self.id)


class User(db.Model, UserMixin, BaseDBMixin):

    __tablename__ = 'User'

    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    last_seen = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.nickname

    def is_admin(self):
        if self.id < 10:
            return True
        return False

    def avatar(self, size):
        md_hash = md5(self.email.encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md_hash, size)


class UserSocial(db.Model, BaseDBMixin):

    __tablename__ = 'UserSocial'

    user_id = db.Column(db.Integer)
    user = db.relationship(
        'User',
        primaryjoin='User.id == UserSocial.user_id',
        foreign_keys='UserSocial.user_id',
    )

    # NOTE: the combination of `network` and `id` should be unique
    social_network = db.Column(db.String(64), nullable=False, unique=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)


class UserInfo(db.Model, BaseDBMixin):

    __tablename__ = 'UserInfo'

    user_id = db.Column(db.Integer)
    user = db.relationship(
        'User',
        primaryjoin='User.id == UserInfo.user_id',
        foreign_keys='UserInfo.user_id',
    )

    about_me = db.Column(db.String(140))


@lm.user_loader
def load_user(user_id):
    # if int(user_id) == 1:
    #     return None
    # return User.query.filter_by(id=int(user_id)).one()
    return User.query.get(int(user_id))


class Post(db.Model, BaseDBMixin):

    __tablename__ = 'Post'

    user_id = db.Column(db.Integer)
    user = db.relationship(
        'User',
        primaryjoin='User.id == Post.user_id',
        foreign_keys='Post.user_id',
    )

    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % self.body
