from django.contrib import admin
from . import models


@admin.register(models.UserAccount)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('email',)
