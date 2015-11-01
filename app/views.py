from flask import (
    render_template,
    flash,
    redirect,
    g,
)
from app import app, db
from app.forms import LoginForm, EditForm
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)
from oauth import OAuthSignIn
from app import tables
from datetime import datetime
from app.tasks import send_sample_email
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


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


def _get_template_config():

    class Config(object):
        pass

    config = Config()
    config.title = 'Home'
    config.bootswatch_template = app.config.get('BOOTSWATCH_TEMPLATE')

    return config


@app.route('/')
@app.route('/index')
def index_page():
    user = {'nickname': 'Prashant'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           config=_get_template_config(),
                           posts=posts,
                           user=user,
                           current_user=current_user)


@app.route('/user/<nickname>')
@login_required
def user_page(nickname):
    user = tables.User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect('index')

    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           config=_get_template_config(),
                           posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('/edit')

    form.nickname.data = g.user.nickname
    form.about_me.data = g.user.about_me

    return render_template('edit.html',
                           config=_get_template_config(),
                           form=form)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


########################################################
# Website Login
########################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')

    return render_template('user.html',
                           form=form,
                           config=_get_template_config(),
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/send_email')
def send_email():
    send_sample_email.apply_async()
    return redirect('/index')


########################################################
# Social Login
########################################################
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect('/index')

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect('/index')

    oauth = OAuthSignIn.get_provider(provider)

    user_oauth_model = oauth.callback()
    social_network, social_id = user_oauth_model.social_id.split('$')
    username = user_oauth_model.username
    email = user_oauth_model.email
    # name = user_oauth_model.name

    if social_id is None:
        flash('Authentication failed.')
        return redirect('/index')

    user_social = tables.UserSocial.query.filter_by(social_id=social_id).first()
    if not user_social:
        user = tables.User(nickname=username, email=email)
        user_social = tables.UserSocial(social_network=social_network,
                                        social_id=social_id)
        user_social.user = user

        db.session.add(user)
        db.session.add(user_social)

        db.session.commit()
    else:
        user = tables.User.query.filter_by(id=user_social.user_id).first()

    login_user(user, True)
    return redirect('/index')
