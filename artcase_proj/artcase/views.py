from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from .models import (
    Work, Creator, Location, Image, Medium, Category, Collection)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

# base views
# model for these views is specified in urls.py

class IndexView(TemplateView):
    '''The home page.'''
    template_name = "artcase/index.html"


class FieldsMixin(object):
    '''Mixin providing model abstraction to views.'''
    view_fields = {
        'work': [
            'title', 'sku',
            'size_h', 'size_w', 'size_d', 'size_unit',
            'condition', 'status', 'notes',
            # 'subjects', # taggit having trouble
            'location', 'medium', 'creators', 'values',
            'categories', 'images', 'collections'
            ],
        'creator': [
            'first_name', 'last_name'],
        'location': [
            'name', 'address', 'sublocation'],
        'image': [
            'image', 'image_h', 'image_w', 'aspect', 'caption'],
        'medium': [
            'name'],
        'category': [
            'name', 'description', 'parent'],
        'collection': [
            'name', 'description'],
        }

    def dispatch(self, *args, **kwargs):
        self.fields = self.view_fields[
            self.model._meta.verbose_name]
        return super().dispatch(*args, **kwargs)


class FormMixin(FieldsMixin):
    '''Mixin providing abstraction for form template.'''
    template_name = "artcase/object_form.html"


class OwnershipMixin(UserPassesTestMixin):
    '''Mixin restricting access to owners depending on content type.'''
    def test_func(self):
        '''Only allow access to owner.'''
        if self.model == Work:
            obj = self.get_object()
            return obj.owner == self.request.user
        else:
            return True


class ArtcaseDetailView(
    LoginRequiredMixin,
    OwnershipMixin,
    FieldsMixin,
    DetailView):
    '''View a single item.'''
    template_name = 'artcase/object_detail.html'
    model = None

    def dispatch(self, *args, **kwargs):
        # titles
        self.title = "{} detail: {}".format(
            self.model._meta.verbose_name,
            self.get_object()
        ).title()

        return super().dispatch(*args, **kwargs)


class ArtcaseListView(LoginRequiredMixin, ListView):    
    '''View several items at once.'''
    template_name = 'artcase/object_list.html'
    model = None

    def dispatch(self, *args, **kwargs):
        # titles
        self.title = "{} list".format(
            self.model._meta.verbose_name
        ).title()

        # define objects in list
        if self.model == Work:
            user = self.request.user
            self.queryset = self.model.objects.filter(
                owner=user.pk)

        return super().dispatch(*args, **kwargs)


class ArtcaseCreateView(
    LoginRequiredMixin,
    FieldsMixin,
    CreateView):
    '''View a new item.'''
    template_name = "artcase/object_form.html"
    model = None

    def dispatch(self, *args, **kwargs):
        # titles
        self.title = "create new {}".format(
            self.model._meta.verbose_name
        ).title()

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # msgs
        messages.add_message(self.request, messages.SUCCESS,
            '"%s" created successfully.' % form.instance)
        
        # don't redirect to list: let user create another
        if 'save_and_new' in form.data.keys():
            reverse_string = 'artcase:{}_create'.format(
                self.model._meta.verbose_name)
            self.success_url = reverse(reverse_string)
        
        # take note of who made it
        if self.model == Work:
            form.instance.owner = self.request.user
        
        return super().form_valid(form)


class ArtcaseUpdateView(
    LoginRequiredMixin,
    OwnershipMixin,
    FieldsMixin,
    UpdateView):
    '''Update an existing item.'''
    template_name = "artcase/object_form.html"
    model = None

    def dispatch(self, *args, **kwargs):
        # titles
        self.title = "update {}: {}".format(
            self.model._meta.verbose_name,
            self.get_object()
        ).title()

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # msgs
        messages.add_message(self.request, messages.SUCCESS,
            '"%s" updated successfully.' % form.instance)

        return super().form_valid(form)


class ArtcaseDeleteView(
    LoginRequiredMixin,
    OwnershipMixin,
    DeleteView):
    '''Delete an existing item.'''
    template_name = "artcase/object_confirm_delete.html"
    model = None
    success_url = None

    def dispatch(self, *args, **kwargs):
        # titles
        self.title = 'Delete {}: "{}"'.format(
            self.model._meta.verbose_name.title(),
            self.get_object())

        # success msg
        self.success_message = '"{}" deleted successfully.'.format(
            self.get_object())

        # next
        self.success_url = reverse_lazy(
            'artcase:%s_list' % self.model._meta.verbose_name)

        return super().dispatch(*args, **kwargs)


    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
            self.success_message)
        return super().delete(request, *args, **kwargs)