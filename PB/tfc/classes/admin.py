from django.contrib import admin
from django.db.models import CASCADE
from django.contrib import admin
from .models import UserEnroll, ClassInstance, ClassOffering, TimeInterval, Keyword


class TimeIntervalAdmin(admin.TabularInline):
    model = TimeInterval


class KeywordAdmin(admin.TabularInline):
    model = Keyword


class ClassAdmin(admin.ModelAdmin):
    inlines = [TimeIntervalAdmin, KeywordAdmin]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ClassOffering, ClassAdmin)
