from djangosanetesting.cases import DatabaseTestCase

from django.contrib.auth.models import User

from metrocar.car_unit_api.validation import valid_user_id
from metrocar.utils.validation import OK


class TestValidUserId(DatabaseTestCase):

    def setUp(self):
        super(TestValidUserId, self).setUp()
        self.user = User.objects.create(username='asdfasfda')

    def tearDown(self):
        self.user.delete()

    def test_valid(self):
        self.assert_equals(valid_user_id(self.user.pk, 'field_name'), OK)

    def test_invalid_format(self):
        valid, error = valid_user_id('gxvbxgcb', 'field_name')
        self.assertFalse(valid)
        self.assert_equals(error,
            '"field_name" should be an integer, not "gxvbxgcb"')

    def test_user_does_not_exist(self):
        valid, error = valid_user_id('648167', 'field_name')
        self.assertFalse(valid)
        self.assert_equals(error, 'User with id "648167" does not exist')

    def test_user_not_active(self):
        self.user.is_active = False
        self.user.save()
        valid, error = valid_user_id(self.user.pk, 'field_name')
        self.assertFalse(valid)
        self.assert_equals(error,
            'User with id "%s" is not active' % self.user.pk)
