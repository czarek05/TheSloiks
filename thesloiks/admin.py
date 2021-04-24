from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TheSloiksUser

admin.site.register(TheSloiksUser, UserAdmin)