from django.contrib import admin
from .models import ClassOffering, TimeInterval, Keyword, ClassInstance
from studios.models import Studio

# Register your models here.

class ClassOfferingInline(admin.TabularInline):
    model = ClassOffering
    fields = ['name', 'description', 'coach', 'times', 'capacity', 'end_recursion']

class ClassInstanceInline(admin.TabularInline):
    model = ClassInstance
    fields = ['date', 'capacity_count']

class TimeIntervalInline(admin.TabularInline):
    model = TimeInterval
    fields = ['start_time', 'end_time', 'day']

class KeywordInline(admin.TabularInline):
    model = Keyword
    fields = ['keyword']

class ClassInstanceInline(admin.TabularInline):
    model = ClassInstance
    fields = ['date', 'capacity_count']

class ClassOfferingAdmin(admin.ModelAdmin):
    inlines = [TimeIntervalInline, KeywordInline, ClassInstanceInline]

admin.site.register(ClassInstance)
admin.site.register(ClassOffering, ClassOfferingAdmin)
admin.site.register(TimeInterval)
admin.site.register(Keyword)