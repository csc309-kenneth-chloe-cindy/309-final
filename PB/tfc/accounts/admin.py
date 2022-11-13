from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TFCUser

# Register your models here.
admin.site.register(TFCUser, UserAdmin)