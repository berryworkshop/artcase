from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Work


class IndexView(TemplateView):
    template_name = "artcase/index.html"


class WorkFormMixin(object):
    fields = [
        'title', 'sku',
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


class WorkListView(ListView):
    model = Work