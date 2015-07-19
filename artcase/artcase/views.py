from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from artcase.models import Artifact, Creator, Organization, Category
from .search import get_query


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
    paginate_by = 12

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'code_number')
        qs = super(ArtifactListView, self).get_queryset().order_by(sort)
        qs = qs.exclude(title_english_short='Untitled')
        return qs


class CreatorView(DetailView):
    model = Creator
    template_name = "artcase/creator.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(CreatorView, self).get_context_data(**kwargs)
        creator = Creator.objects.get(slug=self.kwargs['slug'])
        artifacts = Artifact.objects.filter(creators=creator)#.exclude(title_english_short='Untitled')
        context.update({
            'object_list': artifacts,
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
        artifacts_printed = Artifact.objects.filter(printer=org)#.exclude(title_english_short='Untitled')
        artifacts_published = Artifact.objects.filter(publisher=org)#.exclude(title_english_short='Untitled')
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


class CategoryView(DetailView):
    model = Category
    template_name = "artcase/category.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        artifacts = Artifact.objects.all()
        context.update({
            'artifacts': artifacts,
        })
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "artcase/category_list.html"

    #def get_queryset(self):
    #    sort = self.request.GET.get('sort', 'slug')
    #    qs = super(OrganizationListView, self).get_queryset().order_by(sort)
    #    return qs


class SearchResultsView(TemplateView):
    template_name = "artcase/search_results.html"

    def get(self, request, *args, **kwargs):
        return super(SearchResultsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query_string = ''
        artifact_list = None
        creator_list = None
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            artifact_query = get_query(query_string,
                ['code_number', 'title_english_short',
                 'title_english_full', 'title_original',
                 'description', 'glavlit'])
            artifact_list = Artifact.objects.filter(artifact_query, public=True)

            creator_query = get_query(query_string,
                ['name_latin_last', 'name_latin_first',
                 'name_cyrillic_last', 'name_cyrillic_first',
                 'nationality', 'description'])
            creator_list = Creator.objects.filter(creator_query)

            organization_query = get_query(query_string,
                ['name', 'location', 'description'])
            organization_list = Organization.objects.filter(organization_query)

        context.update({
            'query_string': query_string,
            "artifact_list": artifact_list,
            "creator_list": creator_list,
            "organization_list": organization_list,
        })
        return context