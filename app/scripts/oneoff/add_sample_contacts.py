from app import controllers
from app import app


def add_sample_contacts():

    for idx in xrange(5):
        message = "message {}".format(idx)
        email = 'testing{}@test.com'.format(idx)
        name = 'Sample Name {}'.format(idx)
        controllers.ContactController.create_contact(message, email=email, name=name)


if __name__ == '__main__':
    with app.app_context():
        add_sample_contacts()
