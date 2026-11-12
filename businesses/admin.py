from django.contrib import admin

from .models import Business, Service, WorkingHours


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_active")
    search_fields = ("name", "owner__username")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id","name","business","duration_minutes","price","is_active",)
    search_fields = ("name", "business__name")
    list_filter = ("is_active", "business")
    readonly_fields = ("created_at", "updated_at")


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ("business","weekday","opening_time","closing_time",)
    list_filter = ("business", "weekday")