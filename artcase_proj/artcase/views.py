from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Work

class IndexView(TemplateView):
    template_name = "artcase/index.html"

class WorkCreateView(CreateView):
    model = Work
    fields = [
        'title', 'sku',
        'size_h', 'size_w', 'size_d', 'size_unit',
        'condition', 'status', 'notes',
        'subjects', 'location', 'medium', 'creators', 'values', 'categories', 'images', 'collections'
        ]

class WorkDetailView(DetailView):
    model = Work
    slug_field = 'sku'

class WorkListView(ListView):
    model = Work