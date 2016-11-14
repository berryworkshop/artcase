from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from artcase.views import (
    IndexView, ArtcaseDetailView, ArtcaseListView,
    ArtcaseCreateView, ArtcaseUpdateView, ArtcaseDeleteView)


class TestViewMixin(object):
    fixtures = ['fixture_basic.yaml']

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.c = Client()


class IndexViewTestCase(TestViewMixin, TestCase):
    def test_loads(self):
        '''test'''
        url = reverse('artcase:index')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)


class ArtcaseDetailViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_detail', args=[1])

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''test'''
        pass

    def test_loads(self):
        '''test'''
        self.c.login(username='testuser', password='12345')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)


class ArtcaseListViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_list')

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''test'''
        self.c.login(username='testuser', password='12345')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_only_owner_items(self):
        '''test'''
        pass


class ArtcaseCreateViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_create')

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_loads(self):
        '''test'''
        self.c.login(username='testuser', password='12345')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_blank(self):
        '''test'''
        pass

    def test_form_invalid(self):
        '''test'''
        pass

    def test_form_valid(self):
        '''test'''
        pass

    def test_form_valid_next(self):
        '''test'''
        pass

    def test_cancel(self):
        '''test'''
        pass


class ArtcaseUpdateViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_update', args=[1])

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_denies_non_owner(self):
        '''test'''
        pass

    def test_loads(self):
        '''test'''
        self.c.login(username='testuser', password='12345')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_blank(self):
        '''test'''
        pass

    def test_form_invalid(self):
        '''test'''
        pass

    def test_form_valid(self):
        '''test'''
        pass

    def test_cancel(self):
        '''test'''
        pass


class ArtcaseDeleteViewTestCase(TestViewMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('artcase:work_delete', args=[1])

    def test_denies_anonymous(self):
        '''test'''
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_denies_non_owner(self):
        '''test'''
        pass

    def test_loads(self):
        '''test'''
        pass

    def test_deleting_correct_object(self):
        '''test'''
        pass

    def test_deleted(self):
        '''test'''
        pass

    def test_cancel(self):
        '''test'''
        pass

