from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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


class ArtcaseDetailView(DetailView):
    template_name = 'artcase/object_detail.html'


class ArtcaseListView(ListView):    
    template_name = 'artcase/object_list.html'


class FormMixin(object):
    template_name = "artcase/object_form.html"

    def form_valid(self, form):
        # report back
        messages.add_message(self.request, messages.SUCCESS,
            '"{}" {}d successfully.'.format(form.instance, self.verb))

        # take note of who made it
        form.instance.created_by = self.request.user
        
        if 'save_and_new' in form.data.keys():
            # don't redirect to list: let user create another
            reverse_string = 'artcase:{}_{}'.format(
                self.model._meta.verbose_name, self.verb)
            self.success_url = reverse(reverse_string)
        return super().form_valid(form)


class ArtcaseCreateView(FormMixin, CreateView):
    verb = 'create'


class ArtcaseUpdateView(FormMixin, UpdateView):
    verb = 'update'


class ArtcaseDeleteView(DeleteView):
    template_name = "artcase/object_confirm_delete.html"


# work views

class WorkFieldsMixin(object):
    fields = [
        'title', 'sku', 'owner',
        'size_h', 'size_w', 'size_d', 'size_unit',
        'condition', 'status', 'notes',
        'subjects', 'location', 'medium', 'creators', 'values', 'categories', 'images', 'collections'
        ]


class WorkDetailView(WorkFieldsMixin, ArtcaseDetailView):
    title = 'Work'
    model = Work


class WorkListView(ArtcaseListView):    
    model = Work
    title = 'List of Works'


class WorkCreateView(LoginRequiredMixin, WorkFieldsMixin, ArtcaseCreateView):
    model = Work
    title = 'Create a Work'


class WorkUpdateView(LoginRequiredMixin, WorkFieldsMixin, ArtcaseUpdateView):
    model = Work
    title = "Update Work"


class WorkDeleteView(LoginRequiredMixin, ArtcaseDeleteView):
    model = Work
    success_url = reverse_lazy('artcase:work_list')
    title = "Delete Work"


# creator views

class CreatorFieldsMixin(object):
    fields = ['first_name', 'last_name']


class CreatorDetailView(CreatorFieldsMixin, ArtcaseDetailView):
    model = Creator
    title = "Creator"


class CreatorListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Creator
    title = 'List of Creators'


class CreatorCreateView(LoginRequiredMixin, CreatorFieldsMixin, ArtcaseCreateView):
    model = Creator
    title = 'Create a Creator'


class CreatorUpdateView(LoginRequiredMixin, CreatorFieldsMixin, UpdateView):
    model = Creator
    template_name = "artcase/object_form.html"
    title = "Update Creator"


class CreatorDeleteView(LoginRequiredMixin, DeleteView):
    model = Creator
    success_url = reverse_lazy('artcase:creator_list')
    template_name = "artcase/object_confirm_delete.html"
    title = "Delete Creator"


# location views

class LocationListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Location
    title = 'Location List'


# image views

class ImageListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Image
    title = 'Image List'


# medium views

class MediumListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Medium
    title = 'List of Media'


# category views

class CategoryListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Category
    title = 'List of Categories'


# collection views

class CollectionListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Collection
    title = 'List of Collections'