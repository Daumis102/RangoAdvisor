from django.contrib import admin
from advisor.models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


admin.site.register(Location, LocationAdmin)
