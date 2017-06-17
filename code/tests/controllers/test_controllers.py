from tests.base import AppTestSuiteBase
from tests.helpers import faker
from app import controllers


class UserControllerTestSuite(AppTestSuiteBase):

    def test_fetch_all_users(self):
        u1 = faker.create_user()
        u2 = faker.create_user()
        u3 = faker.create_user()

        user_ids = [u1.id, u2.id, u3.id]
        all_users = controllers.UserController.fetch_all_users(user_ids)

        self.assertEqual(len(all_users), 3)

    def test_create_or_update(self):
        u1 = faker.create_user()

        u1_social = controllers.UserController.fetch_user_social(u1.id)

        u1_ack = controllers.UserController.create_or_update_user(
            u1_social.social_id,
            u1_social.social_network,
            u1_social.access_code,
            u1.email,
            u1.nickname)

        self.assertEqual(u1.id, u1_ack.id)

    def test_user_email_verification_update(self):
        u1 = faker.create_user()

        self.assertFalse(u1.email_verified)
        u1 = controllers.UserController.update_user_email_verification(
            u1.xid,
            u1.email_verification_token)

        self.assertTrue(u1.email_verified)
        u1 = controllers.UserController.update_user_profile(
            u1.xid,
            u1.nickname,
            'new@email.com',
            u1.timezone,
            u1.about_me)

        self.assertFalse(u1.email_verified)


class ContactControllerTestSuite(AppTestSuiteBase):
    pass
