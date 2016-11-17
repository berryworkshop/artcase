from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from artcase.views import (
    IndexView, ArtcaseDetailView, ArtcaseListView,
    ArtcaseCreateView, ArtcaseUpdateView, ArtcaseDeleteView)
from artcase.models import (
    Work,
    # Creator,
    # Location,
    # Image,
    # Medium,
    # Category,
    # Collection,
)


class TestViewMixin(object):
    fixtures = ['fixture_basic.yaml']

    def setUp(self):
        # user_A is created in the fixture (pk=2)
        user_B = User.objects.create(username='testuser_B')
        user_B.set_password('testpass')
        user_B.save()
        self.c = Client()


class IndexViewTestCase(TestViewMixin, TestCase):
    def test_loads(self):
        '''Index page should load for everybody.'''
        url = reverse('artcase:index')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artcase/index.html')


class ArtcaseDetailViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.work = Work.objects.get(pk=1)
        self.url = reverse(
            'artcase:work_detail', args=[self.work.pk])

    def test_has_correct_title(self):
        '''test'''
        pass

    def test_denies_anonymous(self):
        '''Work should not load if user not logged in.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''Work should not load if user is not the owner.'''
        owner = User.objects.get(username='testuser_A')
        self.assertEqual(self.work.owner, owner)
        self.c.login(
            username='testuser_B', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Work should load just fine for owner.'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_detail.html')


class ArtcaseListViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_list')

    def test_has_correct_title(self):
        '''test'''
        pass

    def test_denies_anonymous(self):
        '''Work list should not load if user not logged in.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Work list should load fine for logged-in user.'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_list.html')

    def test_only_owner_objects(self):
        '''Only items owned by the user should be available.'''
        testuser_B = User.objects.get(username="testuser_B")
        work_owned_by_B = Work.objects.create(
            title="test",
            sku="abc123",
            owner=testuser_B,
            )
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        objs_qs = response.context['object_list']
        self.assertTrue(
            objs_qs.filter(pk=2).exists())
        self.assertFalse(
            objs_qs.filter(pk=work_owned_by_B.pk).exists())


class ArtcaseCreateViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_create')

    def test_has_correct_title(self):
        '''test'''
        pass

    def test_message_added(self):
        '''test'''
        pass

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''test'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_form.html')

    def test_form_blank(self):
        '''test'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.post(self.url, {}) # blank data dictionary
        self.assertFormError(
            response, 'form', 'title', 'This field is required.')
        self.assertFormError(
            response, 'form', 'sku', 'This field is required.')

    def test_form_invalid(self):
        '''test'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345'
        }) # invalid data dictionary
        self.assertFormError(
            response, 'form', 'title', 'Ensure this value has at most 100 characters (it has 109).')

    def test_form_valid(self):
        '''test'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'good title',
            'sku': 'good sku',
            'size_unit': 'in',
        }) # valid data dictionary

        # not yet working.
        self.assertRedirects(response, '/')

    def test_owner_recorded(self):
        '''test'''
        pass

    def test_cancel(self):
        '''test'''
        pass


class ArtcaseUpdateViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_update', args=[1])

    def test_has_correct_title(self):
        '''test'''
        pass

    def test_message_added(self):
        '''test'''
        pass

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''test'''
        pass

    def test_loads(self):
        '''test'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_form.html')

    def test_form_blank(self):
        '''test'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.post(self.url, {}) # blank data dictionary
        self.assertFormError(
            response, 'form', 'title', 'This field is required.')
        self.assertFormError(
            response, 'form', 'sku', 'This field is required.')

    def test_form_invalid(self):
        '''test'''
        self.c.login(
            username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345'
        }) # invalid data dictionary
        self.assertFormError(
            response, 'form', 'title', 'Ensure this value has at most 100 characters (it has 109).')

    def test_form_valid(self):
        '''test'''
        pass

    def test_cancel(self):
        '''test'''
        pass


class ArtcaseDeleteViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            'artcase:work_delete', args=[1])

    def test_has_correct_title(self):
        '''test'''
        pass

    def test_message_added(self):
        '''test'''
        pass

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''test'''
        self.c.login(
            username='testuser_B', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''test'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_confirm_delete.html')

    def test_deleting_only_correct_object(self):
        '''test'''
        pass

    def test_deleted(self):
        '''test'''
        pass
        # self.assertRedirects(response, '/')

    def test_next(self):
        '''test'''
        pass

    def test_cancel(self):
        '''test'''
        pass

