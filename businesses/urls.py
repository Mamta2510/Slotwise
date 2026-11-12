from django.urls import path

from .views import ServiceListView, WorkingHoursListCreateView


urlpatterns = [
    path("working-hours/",WorkingHoursListCreateView.as_view(),name="working-hours-list-create",),
    path("services/",ServiceListView.as_view(),name="services-list",),
]