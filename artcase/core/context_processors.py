from django.template import RequestContext
from artcase.models import Category

def sitewide_variables(request):
    return {
        'site_title': 'Cellini Soviet Collection',
        'categories': Category.objects.all(),
    }


