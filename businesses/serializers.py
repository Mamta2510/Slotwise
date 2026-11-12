from rest_framework import serializers

from .models import Business, Service, WorkingHours


class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = ["id","business","weekday","opening_time","closing_time",]
        read_only_fields = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.context["request"].user

        self.fields["business"].queryset = Business.objects.filter(owner=user,is_active=True,)

    def validate(self, data):
        if data["closing_time"] <= data["opening_time"]:
            raise serializers.ValidationError({"closing_time": ("Closing time must be after opening time.")})
        return data


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id","business","name","description","duration_minutes","price",]
        read_only_fields = fields


class AvailabilityQuerySerializer(serializers.Serializer):
    date = serializers.DateField()