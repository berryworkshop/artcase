from django.contrib import admin
from .models import (
    Work, Creator, Value, Location,
    Medium, Image, Category, Collection)

# Register your models here.

admin.site.register(Work)
admin.site.register(Creator)
admin.site.register(Value)
admin.site.register(Location)
admin.site.register(Medium)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Collection)
