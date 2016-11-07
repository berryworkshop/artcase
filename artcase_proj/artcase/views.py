from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from .models import (
    Work, Creator, Location, Image, Medium, Category, Collection)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# base views

class IndexView(TemplateView):
    template_name = "artcase/index.html"


class FieldsMixin(object):
    view_fields = {
        'work': [
            'title', 'sku', 'owner',
            'size_h', 'size_w', 'size_d', 'size_unit',
            'condition', 'status', 'notes',
            'subjects', 'location', 'medium', 'creators', 'values',
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
        self.fields = self.view_fields[self.model._meta.verbose_name]
        return super().dispatch(*args, **kwargs)


class FormMixin(FieldsMixin):
    template_name = "artcase/object_form.html"


class ArtcaseDetailView(LoginRequiredMixin, FieldsMixin, DetailView):
    template_name = 'artcase/object_detail.html'
    title = None
    model = None

    def dispatch(self, *args, **kwargs):
        self.title = "{} detail: {}".format(
            self.model._meta.verbose_name,
            self.get_object()
        ).title()
        return super().dispatch(*args, **kwargs)


class ArtcaseListView(LoginRequiredMixin, ListView):    
    template_name = 'artcase/object_list.html'
    title = None
    model = None

    def dispatch(self, *args, **kwargs):
        self.title = "{} list".format(
            self.model._meta.verbose_name
        ).title()
        return super().dispatch(*args, **kwargs)

class ArtcaseCreateView(LoginRequiredMixin, FieldsMixin, CreateView):
    template_name = "artcase/object_form.html"
    title = None
    model = None

    def dispatch(self, *args, **kwargs):
        self.title = "create new {}".format(
            self.model._meta.verbose_name
        ).title()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
            '"%s" created successfully.' % form.instance)
        # take note of who made it
        form.instance.created_by = self.request.user
        if 'save_and_new' in form.data.keys():
            # don't redirect to list: let user create another
            reverse_string = 'artcase:{}_create'.format(
                self.model._meta.verbose_name)
            self.success_url = reverse(reverse_string)
        return super().form_valid(form)


class ArtcaseUpdateView(LoginRequiredMixin, FieldsMixin, UpdateView):
    template_name = "artcase/object_form.html"
    title = None
    model = None

    def dispatch(self, *args, **kwargs):
        self.title = "update {}: {}".format(
            self.model._meta.verbose_name,
            self.get_object()
        ).title()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
            '"%s" updated successfully.' % form.instance)
        return super().form_valid(form)


class ArtcaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "artcase/object_confirm_delete.html"
    title = None
    model = None
    success_url = None

    def dispatch(self, *args, **kwargs):
        self.title = "delete {}: ".format(
            self.model._meta.verbose_name,
            self.get_object()
        ).title()
        self.success_url = reverse_lazy(
            'artcase:%s_list' % self.model._meta.verbose_name)
        return super().dispatch(*args, **kwargs)
