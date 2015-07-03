from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from artcase.models import Artifact, Creator, Organization


class HomeView(TemplateView):
    template_name = "artcase/home.html"


class ArtifactView(DetailView):
    model = Artifact
    template_name = "artcase/artifact.html"

    def get_object(self):
        return get_object_or_404(
            Artifact, code_number=self.kwargs['code_number'])

    def get_context_data(self, **kwargs):
        context = super(ArtifactView, self).get_context_data(**kwargs)
        artifact = Artifact.objects.get(code_number=self.kwargs['code_number'])
        creators = Creator.objects.filter(artifact=artifact)
        context.update({
            'creators': creators,
        })
        return context


class ArtifactListView(ListView):
    model = Artifact
    template_name = "artcase/artifact_list.html"

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'code_number')
        qs = super(ArtifactListView, self).get_queryset().order_by(sort)
        qs = qs.exclude(title_english_short='Untitled')
        return qs


class CreatorView(DetailView):
    model = Creator
    template_name = "artcase/creator.html"

    def get_context_data(self, **kwargs):
        context = super(CreatorView, self).get_context_data(**kwargs)
        creator = Creator.objects.get(slug=self.kwargs['slug'])
        artifacts = Artifact.objects.filter(creators=creator)
        context.update({
            'artifacts': artifacts,
        })
        return context


class CreatorListView(ListView):
    model = Creator
    template_name = "artcase/creator_list.html"


class OrganizationView(DetailView):
    model = Organization
    template_name = "artcase/organization.html"

    def get_context_data(self, **kwargs):
        context = super(OrganizationView, self).get_context_data(**kwargs)
        org = Organization.objects.get(slug=self.kwargs['slug'])
        artifacts_printed = Artifact.objects.filter(printer=org)
        artifacts_published = Artifact.objects.filter(publisher=org)
        context.update({
            'artifacts_printed':artifacts_printed,
            'artifacts_published':artifacts_published,
        })
        return context


class OrganizationListView(ListView):
    model = Organization
    template_name = "artcase/organization_list.html"

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'slug')
        qs = super(OrganizationListView, self).get_queryset().order_by(sort)
        return qs