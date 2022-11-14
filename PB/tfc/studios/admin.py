from django.contrib import admin
from .models import Studio, StudioImage, StudioAmenities

# Register your models here.

class StudioImageInline(admin.TabularInline):
    model = StudioImage
    fields = ['image_as_blob']

class StudioAdmin(admin.ModelAdmin):
    inlines = [StudioImageInline]
    fields = fields = ['name', 'address', 'postal_code', 'phone_num', 'longitude', 'latitude']


admin.site.register(Studio, StudioAdmin)
admin.site.register(StudioAmenities)
admin.site.register(StudioImage)