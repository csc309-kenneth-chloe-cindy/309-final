from django.contrib import admin
from django.db.models import CASCADE
from .models import UserEnroll, ClassInstance, ClassOffering

admin.site.register(UserEnroll)
admin.site.register(ClassInstance)
admin.site.register(ClassOffering)
