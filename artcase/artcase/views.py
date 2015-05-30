from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from artcase.models import Artifact

class HomeView(TemplateView):
    template_name = "artcase/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({ })
        return context

class ArtifactView(DetailView):
    model = Artifact
    template_name = "artcase/artifact.html"

    def get_object(self):
        return get_object_or_404(Artifact, code_number=self.kwargs['code_number'])

    def get_context_data(self, **kwargs):
        context = super(ArtifactView, self).get_context_data(**kwargs)
        context.update({
            })
        return context

class ArtifactListView(ListView):
    model = Artifact
    template_name = "artcase/artifact_list.html"

    def get_context_data(self, **kwargs):
        context = super(ArtifactListView, self).get_context_data(**kwargs)
        context.update({ })
        return context