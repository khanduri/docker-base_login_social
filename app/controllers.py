from app import tables, db


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
