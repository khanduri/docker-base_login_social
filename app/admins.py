from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask.ext.login import current_user
from flask import redirect


class _AdminMixin(object):

    def is_accessible(self):
        if not current_user:
            return False
        return current_user.is_admin() if hasattr(current_user, 'is_admin') else False

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/index')


class AdminAccessIndexView(_AdminMixin, AdminIndexView):
    pass


class AdminAccessView(_AdminMixin, ModelView):
    pass


