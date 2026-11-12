from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Service, WorkingHours
from .serializers import ServiceSerializer, WorkingHoursSerializer


class WorkingHoursListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkingHoursSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            WorkingHours.objects
            .filter(business__owner=self.request.user)
            .select_related("business")
            .order_by("business_id", "weekday")
        )


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Service.objects
            .filter(is_active=True,business__is_active=True,)
            .order_by("id")
        )


