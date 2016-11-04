from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import (
    Work, Creator, Location, Image, Medium, Category, Collection)
from django.contrib.auth.mixins import LoginRequiredMixin


# base views

class IndexView(TemplateView):
    template_name = "artcase/index.html"


class ArtcaseDetailView(DetailView):
    template_name = 'artcase/object_detail.html'


class ArtcaseListView(ListView):    
    template_name = 'artcase/object_list.html'


class ArtcaseCreateView(CreateView):
    template_name = "artcase/object_form.html"


class ArtcaseUpdateView(UpdateView):
    template_name = "artcase/object_form.html"


class ArtcaseDeleteView(DeleteView):
    template_name = "artcase/object_confirm_delete.html"


# work views

class WorkFormMixin(LoginRequiredMixin, object):
    fields = [
        'title', 'sku', 'owner',
        'size_h', 'size_w', 'size_d', 'size_unit',
        'condition', 'status', 'notes',
        'subjects', 'location', 'medium', 'creators', 'values', 'categories', 'images', 'collections'
        ]


class WorkDetailView(ArtcaseDetailView):
    title = 'Work'
    model = Work


class WorkListView(ArtcaseListView):    
    model = Work
    title = 'List Works'


class WorkCreateView(WorkFormMixin, ArtcaseCreateView):
    model = Work
    title = "Create Work"


class WorkUpdateView(WorkFormMixin, ArtcaseUpdateView):
    model = Work
    title = "Update Work"


class WorkDeleteView(ArtcaseDeleteView):
    model = Work
    success_url = reverse_lazy('artcase:work_list')
    title = "Delete Work"


# creator views

class CreatorFormMixin(LoginRequiredMixin, object):
    fields = ['first_name', 'last_name']


class CreatorDetailView(ArtcaseDetailView):
    model = Creator
    title = "Creator"


class CreatorListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Creator
    title = 'List Creators'


class CreatorCreateView(CreatorFormMixin, CreateView):
    model = Creator
    template_name = "artcase/object_form.html"
    title = "Create Creator"


class CreatorUpdateView(CreatorFormMixin, UpdateView):
    model = Creator
    template_name = "artcase/object_form.html"
    title = "Update Creator"


class CreatorDeleteView(DeleteView):
    model = Creator
    success_url = reverse_lazy('artcase:work_list')
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
    title = 'Medium List'


# category views

class CategoryListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Category
    title = 'Category List'


# collection views

class CollectionListView(ListView):
    template_name = 'artcase/object_list.html'
    model = Collection
    title = 'Collection List'