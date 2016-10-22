from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Work
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = "artcase/index.html"


class WorkFormMixin(LoginRequiredMixin, object):
    fields = [
        'title', 'sku', 'owner',
        'size_h', 'size_w', 'size_d', 'size_unit',
        'condition', 'status', 'notes',
        'subjects', 'location', 'medium', 'creators', 'values', 'categories', 'images', 'collections'
        ]


class WorkCreateView(WorkFormMixin, CreateView):
    model = Work
    title = "Work Create"


class WorkDetailView(DetailView):
    model = Work
    slug_field = 'sku'


class WorkUpdateView(WorkFormMixin, UpdateView):
    model = Work
    title = "Work Update"
    slug_field = 'sku'


class WorkDeleteView(DeleteView):
    model = Work
    success_url = reverse_lazy('artcase:work_list')
    slug_field = 'sku'


class WorkListView(ListView):
    model = Work