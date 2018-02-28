from django.contrib import admin
from advisor.models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    prepopulated_fields = {'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('publish_date', 'content', 'location_id', 'rating', 'posted_by')
    

class PictureAdmin(admin.ModelAdmin):
    list_display = ('upload_date', 'location_id', 'uploaded_by', 'picture')   
    
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(UserProfile)
