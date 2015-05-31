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
        return get_object_or_404(Artifact, code_number=self.kwargs['code_number'])


class ArtifactListView(ListView):
    model = Artifact
    template_name = "artcase/artifact_list.html"


class CreatorView(DetailView):
    model = Creator
    template_name = "artcase/creator.html"


class CreatorListView(ListView):
    model = Creator
    template_name = "artcase/creator_list.html"
