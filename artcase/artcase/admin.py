from django.contrib import admin
from .models import Artifact, ArtifactImage, Creator, Organization, Category

class CreatorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [ ('name_latin_last', 'name_latin_first'),
                            ('name_cyrillic_last', 'name_cyrillic_first'),
                            'nationality',
                            ('year_birth', 'year_death'),
                            'description','slug',]}),
        #('Main', {'fields': ['artifacts']})
    ]
    list_display = ('__str__', 'nationality', 'get_lifespan')
    list_filter =  ['nationality']
    #filter_horizontal = ['artifacts']
    search_fields = ['name_latin_last', 'name_latin_first',
        'name_cyrillic_last', 'name_cyrillic_first', 'nationality',
        'year_birth', 'year_death', 'description']
    prepopulated_fields = {"slug": ("name_latin_last", "name_latin_first")}

class ArtifactImageAdmin(admin.ModelAdmin):
    list_display = ('filename', 'role',  'artifact')
    list_editable = ['role']
    list_filter =  ['role']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_russian', 'description')
    list_editable = ['name', 'name_russian', 'description']


admin.site.register(Artifact)
admin.site.register(ArtifactImage, ArtifactImageAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Organization)
admin.site.register(Category, CategoryAdmin)