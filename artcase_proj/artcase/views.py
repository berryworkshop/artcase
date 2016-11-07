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
            'subjects', 'location', 'medium', 'creators', 'values', 'categories', 'images', 'collections'
            ],
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


class ArtcaseListView(LoginRequiredMixin, ListView):    
    template_name = 'artcase/object_list.html'
    title = None
    model = None

class ArtcaseCreateView(LoginRequiredMixin, FieldsMixin, CreateView):
    template_name = "artcase/object_form.html"
    title = None
    model = None

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
        self.success_url = reverse_lazy(
            'artcase:%s_list' % self.model._meta.verbose_name)
        return super().dispatch(*args, **kwargs)


# work views

# class WorkFieldsMixin(object):
#     fields = [
#         'title', 'sku', 'owner',
#         'size_h', 'size_w', 'size_d', 'size_unit',
#         'condition', 'status', 'notes',
#         'subjects', 'location', 'medium', 'creators', 'values', 'categories', 'images', 'collections'
#         ]


# class WorkDetailView(WorkFieldsMixin, ArtcaseDetailView):
#     title = 'Work'
#     model = Work


# class WorkListView(ArtcaseListView):    
#     title = 'List of Works'
#     model = Work


# class WorkCreateView(WorkFieldsMixin, ArtcaseCreateView):
#     title = 'Create a Work'
#     model = Work


# class WorkUpdateView(WorkFieldsMixin, ArtcaseUpdateView):
#     title = "Update Work"
#     model = Work


# class WorkDeleteView(ArtcaseDeleteView):
#     title = "Delete Work"
#     model = Work
#     success_url = reverse_lazy('artcase:work_list')


# creator views

class CreatorFieldsMixin(object):
    fields = ['first_name', 'last_name']


class CreatorDetailView(CreatorFieldsMixin, ArtcaseDetailView):
    title = "Creator"
    model = Creator


class CreatorListView(ArtcaseListView):
    title = 'List of Creators'
    model = Creator


class CreatorCreateView(CreatorFieldsMixin, ArtcaseCreateView):
    title = 'Create a Creator'
    model = Creator


class CreatorUpdateView(CreatorFieldsMixin, ArtcaseUpdateView):
    title = "Update Creator"
    model = Creator


class CreatorDeleteView(ArtcaseDeleteView):
    title = "Delete Creator"
    model = Creator
    success_url = reverse_lazy('artcase:creator_list')


# location views

class LocationFieldsMixin(object):
    fields = ['name', 'address', 'sublocation']


class LocationDetailView(LocationFieldsMixin, ArtcaseDetailView):
    title = "Location"
    model = Location


class LocationListView(ArtcaseListView):
    title = 'Location List'
    model = Location


class LocationCreateView(LocationFieldsMixin, ArtcaseCreateView):
    title = 'Create a Location'
    model = Location


class LocationUpdateView(LocationFieldsMixin, ArtcaseUpdateView):
    title = "Update Location"
    model = Location


class LocationDeleteView(ArtcaseDeleteView):
    title = "Delete Location"
    model = Location
    success_url = reverse_lazy('artcase:location_list')


# image views

class ImageFieldsMixin(object):
    fields = ['image', 'image_h', 'image_w', 'aspect', 'caption']


class ImageDetailView(ImageFieldsMixin, ArtcaseDetailView):
    title = 'Image'
    model = Image


class ImageListView(ArtcaseListView):
    title = 'Image List'
    model = Image


class ImageCreateView(ImageFieldsMixin, ArtcaseCreateView):
    title = 'Create an Image'
    model = Image


class ImageUpdateView(ImageFieldsMixin, ArtcaseUpdateView):
    title = "Update Image"
    model = Image


class ImageDeleteView(ArtcaseDeleteView):
    title = "Delete Image"
    model = Image
    success_url = reverse_lazy('artcase:image_list')


# medium views

class MediumFieldsMixin(object):
    fields = ['name']


class MediumDetailView(MediumFieldsMixin, ArtcaseDetailView):
    title = 'Medium'
    model = Medium


class MediumListView(ArtcaseListView):
    title = 'List of Media'
    model = Medium


class MediumCreateView(MediumFieldsMixin, ArtcaseCreateView):
    title = 'Create a Medium'
    model = Medium


class MediumUpdateView(MediumFieldsMixin, ArtcaseUpdateView):
    title = "Update Medium"
    model = Medium


class MediumDeleteView(ArtcaseDeleteView):
    title = "Delete Medium"
    model = Medium
    success_url = reverse_lazy('artcase:medium_list')


# category views

class CategoryFieldsMixin(object):
    fields = ['name', 'description', 'parent']


class CategoryDetailView(CategoryFieldsMixin, ArtcaseDetailView):
    title = 'Category'
    model = Category


class CategoryListView(ArtcaseListView):
    title = 'List of Categories'
    model = Category


class CategoryCreateView(CategoryFieldsMixin, ArtcaseCreateView):
    title = 'Create a Category'
    model = Category


class CategoryUpdateView(CategoryFieldsMixin, ArtcaseUpdateView):
    title = "Update Category"
    model = Category


class CategoryDeleteView(ArtcaseDeleteView):
    title = "Delete Category"
    model = Category
    success_url = reverse_lazy('artcase:category_list')


# collection views

class CollectionFieldsMixin(object):
    fields = ['name', 'description']


class CollectionDetailView(CategoryFieldsMixin, ArtcaseDetailView):
    title = 'Collection'
    model = Collection


class CollectionListView(ArtcaseListView):
    title = 'List of Collections'
    model = Collection


class CollectionCreateView(CollectionFieldsMixin, ArtcaseCreateView):
    title = 'Create a Collection'
    model = Collection


class CollectionUpdateView(CollectionFieldsMixin, ArtcaseUpdateView):
    title = "Update Collection"
    model = Collection


class CollectionDeleteView(ArtcaseDeleteView):
    title = "Delete Collection"
    model = Collection
    success_url = reverse_lazy('artcase:collection_list')