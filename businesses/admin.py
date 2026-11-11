from django.contrib import admin

from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_active")
    search_fields = ("name", "owner__username")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")