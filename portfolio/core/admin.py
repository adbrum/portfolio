from django.contrib import admin
from portfolio.core.models import Email


class EmailModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'created_at']

admin.site.register(Email, EmailModelAdmin)
