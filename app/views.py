from datetime import datetime

from flask import (
    render_template,
    flash,
    redirect,
    request,
    g,
)
from app import (
    app,
    controllers,
    db,
    forms,
)
from app.tasks.emails.verification_email import send_email_verification_link
from app.tasks.emails.sample import send_sample_email
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)
from app.helpers.oauth import OAuthSignIn


def _get_template_config(title='Home'):

    class Config(object):
        pass

    config = Config()
    config.title = title
    config.bootswatch_template = app.config.get('BOOTSWATCH_TEMPLATE')

    return config


@app.route('/')
@app.route('/index')
def index_page():
    return render_template('index.html',
                           config=_get_template_config(),
                           current_user=current_user)


@app.route('/user/<nickname>')
@login_required
def user_page(nickname):
    user = controllers.UserController.fetch_user_with_nickname(nickname)
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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    form = forms.ProfileForm()
    if form.validate_on_submit():

        send_verification_mail = True if g.user.email != form.email.data else False

        controllers.UserController.update_user_profile(g.user.xid,
                                                       form.nickname.data,
                                                       form.email.data,
                                                       form.timezone.data,
                                                       form.about_me.data)

        if send_verification_mail:
            send_email_verification_link.apply_async((g.user.xid, ))

        flash('Your changes have been saved.')
        return redirect('/profile')

    return render_template('edit.html',
                           config=_get_template_config(),
                           form=form,
                           user=g.user)


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = forms.ContactForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('contact.html',
                                   config=_get_template_config(),
                                   form=form)
        else:

            name = form.name.data
            email = form.email.data
            message = form.message.data
            user = g.user if g.user.is_authenticated else None

            controllers.ContactController.create_contact(message, email=email, name=name, user=user)
            flash('Thank you for the feedback!')

            return redirect('/index')

    elif request.method == 'GET':
        return render_template('contact.html',
                               config=_get_template_config(),
                               form=form)


@app.route('/about')
def about_page():
    return render_template('about.html',
                           config=_get_template_config())


@app.route('/story')
def story_page():
    return render_template('story.html',
                           config=_get_template_config())


@app.route('/<path:path>')
def missing(path=None):
    return render_template('missing.html',
                           config=_get_template_config())


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
def login_page():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')

    return render_template('user.html',
                           form=form,
                           config=_get_template_config(),
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect('/index')


def _validate_user(user_xid):
    "DUPE"
    user = g.user if g.user.is_authenticated else None
    request_user_id = controllers.UserController.id_from_xid(user_xid)
    return user.id == request_user_id


@app.route('/verify/<user_xid>/<verification_token>')
@login_required
def verify_email_page(user_xid, verification_token):

    if not _validate_user(user_xid):
        return render_template('verify.html', verified=False)

    user = controllers.UserController.update_user_email_verification(user_xid, verification_token)
    verified = user.email_verification_token is None
    return render_template('verify.html', verified=verified)


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
    access_code = user_oauth_model.access_code
    # name = user_oauth_model.name

    if social_id is None:
        flash('Authentication failed.')
        return redirect('/index')

    user = controllers.UserController.create_or_update_user(social_id, social_network, access_code, email, username)

    login_user(user, True)
    return redirect('/index')


########################################################
# Template samples
########################################################
@app.route('/email/template/<key>')
def email_templates(key):

    fake_verify_link_data = {'link_data': {'user_xid': 'fake_xid',
                                           'verification_token': 'FAKE_LINK_TOKEN',
                                           '_external': True}}

    email_data = {
        'email_verify': ("email/email_verification.html", fake_verify_link_data),
    }.get(key)

    if not email_data:
        return render_template('missing.html',
                               config=_get_template_config())

    template_name, template_kwargs = email_data
    return render_template(template_name, **template_kwargs)


##############################
# SAMPLE: to show async flow
@app.route('/send_email')
@login_required
def send_email_page():
    send_sample_email.apply_async()
    return redirect('/index')
