from django.http import HttpResponse
from django.views.generic import TemplateView

class HomePageView(TemplateView):

    template_name = "artcase/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        print(context.__class__)
        context.update({
            'hello_world': 'Hello World'
            })
        return context