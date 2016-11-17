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

# These View tests combine aspects of functional/integration tests, as pure View tests are difficult to write in isolation, and integration tests would necessarily need to heavily depend on Views.


class TestViewMixin(object):
    fixtures = ['fixture_basic.yaml']

    def setUp(self):
        # users
        # user_A is created in the fixture (pk=2)
        user_B = User.objects.create(username='testuser_B')
        user_B.set_password('testpass')
        user_B.save()

        # client
        self.c = Client()


class IndexViewTestCase(TestViewMixin, TestCase):
    def test_loads(self):
        '''Index page should load for everybody.'''
        url = reverse('artcase:index')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artcase/index.html')


class ArtcaseDetailViewTestCase(TestViewMixin, TestCase):
    '''Tests dealing with showing a single item.'''
    def setUp(self):
        super().setUp()
        self.work = Work.objects.get(pk=1)
        self.url = reverse(
            'artcase:work_detail', args=[self.work.pk])

    def test_has_correct_title(self):
        '''Should have correct title.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        view = response.context['view']
        self.assertEqual(view.title, 'Work Detail: Work A')

    def test_denies_anonymous(self):
        '''Work should not load if user not logged in.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''Work should not load if user is not the owner.'''
        owner = User.objects.get(username='testuser_A')
        self.assertEqual(self.work.owner, owner)
        self.c.login(username='testuser_B', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Work should load just fine for owner.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_detail.html')


class ArtcaseListViewTestCase(TestViewMixin, TestCase):
    '''Tests dealing with showing several items at once.'''
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_list')

    def test_has_correct_title(self):
        '''Should have correct title.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        view = response.context['view']
        self.assertEqual(view.title, 'Work List')

    def test_denies_anonymous(self):
        '''Work list should not load if user not logged in.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Work list should load fine for logged-in user.'''
        self.c.login(username='testuser_A', password='testpass')
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
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        objs_qs = response.context['object_list']
        self.assertTrue(
            objs_qs.filter(pk=2).exists())
        self.assertFalse(
            objs_qs.filter(pk=work_owned_by_B.pk).exists())


class ArtcaseCreateViewTestCase(TestViewMixin, TestCase):
    '''Tests dealing with creating a new item.'''
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_create')

    def test_has_correct_title(self):
        '''Should have correct title.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        view = response.context['view']
        self.assertEqual(view.title, 'Create New Work')

    def test_message_added(self):
        '''Should produce correct message.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'test title',
            'sku': 'test-sku',
            'size_unit': 'in',
        }, follow=True) # valid data dictionary
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), '"test title" created successfully.')

    def test_denies_anonymous(self):
        '''Should not allow non-logged-in users.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Should load for correctly authenticated and authorized user.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_form.html')

    def test_form_blank(self):
        '''Blank form should not be accepted.'''
        self.c.login(username='testuser_A', password='testpass')
        qty_before = Work.objects.all().count()
        response = self.c.post(self.url, {}) # blank data dictionary
        qty_after = Work.objects.all().count()
        self.assertFormError(
            response, 'form', 'title', 'This field is required.')
        self.assertFormError(
            response, 'form', 'sku', 'This field is required.')
        self.assertEqual(qty_before, qty_after)

    def test_form_invalid(self):
        '''Invalid form should not be accepted.'''
        self.c.login(username='testuser_A', password='testpass')
        qty_before = Work.objects.all().count()
        response = self.c.post(self.url, {
            'title': 'abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345'
        }) # invalid data dictionary
        qty_after = Work.objects.all().count()
        self.assertFormError(
            response, 'form', 'title', 'Ensure this value has at most 100 characters (it has 109).')
        self.assertEqual(qty_before, qty_after)

    def test_form_success_redirect(self):
        '''Upon successful submit, should redirect to object view.'''
        self.c.login(username='testuser_A', password='testpass')
        qty_before = Work.objects.all().count()
        response = self.c.post(self.url, {
            'title': 'test title',
            'sku': 'test-sku',
            'size_unit': 'in',
        }, follow=True) # valid data dictionary
        qty_after = Work.objects.all().count()
        obj = Work.objects.get(title='test title')
        success_url = reverse('artcase:work_detail', args=[obj.pk])
        self.assertRedirects(response, success_url, status_code=302)
        self.assertEqual(qty_before, qty_after-1)

    def test_form_success_redirect_new(self):
        '''If "save and new" button pressed instead of standard submit, should redirect to create form.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'test title',
            'sku': 'test-sku',
            'size_unit': 'in',
            'save_and_new': True,
        }, follow=True) # valid data dictionary
        success_url = reverse('artcase:work_create')
        self.assertRedirects(response, success_url, status_code=302)

    def test_owner_recorded(self):
        '''Owner should be correctly noted in Work.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'test title',
            'sku': 'test-sku',
            'size_unit': 'in',
        }) # valid data dictionary
        work = Work.objects.get(title='test title')
        owner = User.objects.get(username='testuser_A')
        self.assertEqual(work.owner.pk, owner.pk)


class ArtcaseUpdateViewTestCase(TestViewMixin, TestCase):
    '''Tests dealing with editing an existing item.'''
    def setUp(self):
        super().setUp()
        self.work = Work.objects.get(pk=1)
        self.url = reverse('artcase:work_update', args=[self.work.pk])

    def test_has_correct_title(self):
        '''Should have correct title.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        view = response.context['view']
        self.assertEqual(view.title, 'Update Work: Work A')

    def test_message_added(self):
        '''Should produce correct message.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'test title',
            'sku': 'test-sku',
            'size_unit': 'in',
        }, follow=True) # valid data dictionary
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), '"test title" updated successfully.')

    def test_denies_anonymous(self):
        '''Should not load for non-logged-in-users.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''Work should not load if user is not the owner.'''
        owner = User.objects.get(username='testuser_A')
        self.assertEqual(self.work.owner, owner)
        self.c.login(username='testuser_B', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Should update OK for correctly authorized users.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_form.html')

    def test_form_blank(self):
        '''Should not allow blank submissions.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, {}) # blank data dictionary
        self.assertFormError(
            response, 'form', 'title', 'This field is required.')
        self.assertFormError(
            response, 'form', 'sku', 'This field is required.')

    def test_form_invalid(self):
        '''Should not allow invalid submissions.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, {
            'title': 'abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345 abcde12345'
        }) # invalid data dictionary
        self.assertFormError(
            response, 'form', 'title', 'Ensure this value has at most 100 characters (it has 109).')

    def test_form_success_redirect(self):
        '''Upon successful submit, should redirect to object view.'''
        self.c.login(username='testuser_A', password='testpass')
        qty_before = Work.objects.all().count()
        response = self.c.post(self.url, {
            'title': 'test title',
            'sku': 'test-sku',
            'size_unit': 'in',
        }, follow=True) # valid data dictionary
        qty_after = Work.objects.all().count()
        obj = Work.objects.get(title='test title')
        success_url = reverse('artcase:work_detail', args=[obj.pk])
        self.assertRedirects(response, success_url, status_code=302)
        self.assertEqual(qty_before, qty_after)


class ArtcaseDeleteViewTestCase(TestViewMixin, TestCase):
    '''Tests dealing with deleting an existing item.'''
    def setUp(self):
        super().setUp()
        self.work = Work.objects.get(pk=1)
        self.url = reverse(
            'artcase:work_delete', args=[self.work.pk])

    def test_has_correct_title(self):
        '''Should have correct title.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        view = response.context['view']
        self.assertEqual(view.title, 'Delete Work: "Work A"')

    def test_message_added(self):
        '''Should produce correct message.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.post(self.url, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), '"Work A" deleted successfully.')

    def test_denies_anonymous(self):
        '''Should not permit non-logged-in users.'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''Should not permit non-owners.'''
        self.c.login(
            username='testuser_B', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''Should be accessible for Work owners to delete a Work.'''
        self.c.login(username='testuser_A', password='testpass')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'artcase/object_confirm_delete.html')

    def test_deleted(self):
        '''Should delete object, and no others.'''
        self.c.login(username='testuser_A', password='testpass')
        work_pk = self.work.pk
        qty_before = Work.objects.all().count()
        response = self.c.post(self.url, follow=True)
        qty_after = Work.objects.all().count()
        success_url = reverse('artcase:work_list')
        self.assertRedirects(response, success_url, status_code=302)
        self.assertEqual(qty_before, qty_after+1)
        self.assertFalse(Work.objects.filter(pk=work_pk).exists())
