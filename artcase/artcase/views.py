from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from artcase.models import Artifact, Creator


class HomeView(TemplateView):
    template_name = "artcase/home.html"


class ArtifactView(DetailView):
    model = Artifact
    template_name = "artcase/artifact.html"

    def get_object(self):
        return get_object_or_404(
            Artifact, code_number=self.kwargs['code_number'])


class ArtifactListView(ListView):
    model = Artifact
    template_name = "artcase/artifact_list.html"

    def get_queryset(self):
        sort = self.request.GET.get('sort', None)
        default_sort = 'code_number'
        if sort:
            qs = super(ArtifactListView, self).get_queryset().order_by(sort)
        else:
            qs = super(ArtifactListView, self).get_queryset().order_by(default_sort)
        return qs


class CreatorView(DetailView):
    model = Creator
    template_name = "artcase/creator.html"


class CreatorListView(ListView):
    model = Creator
    template_name = "artcase/creator_list.html"
