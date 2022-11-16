from django.contrib import admin
from django.db.models import CASCADE
from django.contrib import admin
from .models import UserEnroll, ClassInstance, ClassOffering, TimeInterval, Keyword


class TimeIntervalAdmin(admin.TabularInline):
    model = TimeInterval


class KeywordAdmin(admin.TabularInline):
    model = Keyword


class ClassOfferingAdmin(admin.ModelAdmin):
    inlines = [TimeIntervalAdmin, KeywordAdmin]
    actions = ['delete_future']

    @admin.action(description="Delete all future class instances")
    def delete_future(self, request, queryset):
        for class_offering in queryset:
            if isinstance(class_offering, ClassOffering):
                class_offering.delete_future_instances()

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True


class ClassInstanceAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(ClassOffering, ClassOfferingAdmin)
admin.site.register(ClassInstance, ClassInstanceAdmin)
