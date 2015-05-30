from django.template import RequestContext

def sitewide_variables(request):
   return {'site_title': 'Cellini Soviet Collection'}