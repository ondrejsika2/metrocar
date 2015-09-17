from metrocar.user_management.models import UserRegistrationRequest,\
    MetrocarUser
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1
import django.test


class TestUserRegistrationRequest(django.test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        MetrocarUser.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        MetrocarUser.objects.all().delete()

    def setUp(self):
        MetrocarUser.objects.all().delete()
        UserRegistrationRequest.objects.all().delete()

        self.user_1 = create_user_1()
        request = UserRegistrationRequest.objects.get_or_create(
            user=self.user_1
        )[0]
        request.delete()


    def test_0_approve(self):
        self.user_1.is_active = False
        self.user_1.save()

        req = UserRegistrationRequest.objects.create_for_user(self.user_1)
        self.assertEquals(req.approved, False)
        self.assertEquals(req.resolved, False)

        req.approve()

        self.assertEquals(req.approved, True)
        self.assertEquals(req.resolved, True)

        u = MetrocarUser.objects.get(pk=self.user_1.pk)
        self.assertEquals(u.is_active, True)
        req.delete()

    def test_1_reject(self):
        self.user_1.is_active = False
        self.user_1.save()

        req = UserRegistrationRequest.objects.create_for_user(self.user_1)
        self.assertEquals(req.approved, False)
        self.assertEquals(req.resolved, False)

        req.reject()

        self.assertEquals(req.approved, False)
        self.assertEquals(req.resolved, True)

        u = MetrocarUser.objects.with_inactive().get(pk=self.user_1.pk)
        self.assertEquals(u.is_active, False)
        req.delete()

    def test_3_unique(self):
        pass
        UserRegistrationRequest.objects.create_for_user(self.user_1)
        with self.assertRaises(Exception):
            UserRegistrationRequest.objects.create_for_user(self.user_1)
