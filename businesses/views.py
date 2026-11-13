from datetime import datetime, timedelta, timezone as dt_timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Service, WorkingHours
from .serializers import AvailabilityQuerySerializer, ServiceSerializer, WorkingHoursSerializer
from businesses import serializers


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


class ServiceAvailabilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_id):
        query = AvailabilityQuerySerializer(
            data=request.query_params
        )
        query.is_valid(raise_exception=True)
        selected_date = query.validated_data["date"]

        service = get_object_or_404(
            Service.objects.select_related("business"),
            pk=service_id,
            is_active=True,
            business__is_active=True,
        )
        business = service.business

        try:
            business_timezone = ZoneInfo(business.timezone)
        except ZoneInfoNotFoundError:
            raise serializers.ValidationError({
                "detail": "The business timezone is invalid."
            })

        now = timezone.now()
        local_today = now.astimezone(business_timezone).date()

        if selected_date < local_today:
            raise serializers.ValidationError({
                "date": "Please select today or a future date."
            })

        working_hours = WorkingHours.objects.filter(
            business=business,
            weekday=selected_date.weekday(),
        ).first()

        slots = []

        if working_hours is not None:
            if service.duration_minutes < 1:
                raise serializers.ValidationError({
                    "detail": "The service duration must be positive."
                })

            opening = datetime.combine(
                selected_date,
                working_hours.opening_time,
                tzinfo=business_timezone,
            )
            closing = datetime.combine(
                selected_date,
                working_hours.closing_time,
                tzinfo=business_timezone,
            )

            slot_start = opening.astimezone(dt_timezone.utc)
            closing_utc = closing.astimezone(dt_timezone.utc)
            duration = timedelta(
                minutes=service.duration_minutes
            )

            while slot_start + duration <= closing_utc:
                slot_end = slot_start + duration

                if slot_start > now:
                    slots.append({
                        "start": slot_start.astimezone(
                            business_timezone
                        ).isoformat(),
                        "end": slot_end.astimezone(
                            business_timezone
                        ).isoformat(),
                    })

                slot_start = slot_end

        return Response({
            "service_id": service.id,
            "date": selected_date.isoformat(),
            "timezone": business.timezone,
            "slots": slots,
        })