from django.contrib import admin
from advisor.models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('publish_date', 'content', 'location_id', 'rating', 'posted_by')


admin.site.register(Location, LocationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
admin.site.register(Picture)
