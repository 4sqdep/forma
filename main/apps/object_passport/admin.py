from django.contrib import admin
from main.apps.object_passport.models.object import Object
from main.apps.object_passport.models.object_gallery import Gallery



class ObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code')

admin.site.register(Object, ObjectAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'object', 'file', 'name')

admin.site.register(Gallery, GalleryAdmin)