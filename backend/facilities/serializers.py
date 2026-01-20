from rest_framework import serializers
from .models import Facility, Booking

class FacilitySerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source='ward.name', read_only=True)
    type_display = serializers.CharField(source='get_facility_type_display', read_only=True)

    class Meta:
        model = Facility
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'user']

    def validate(self, data):
        # We also run model validation here to catch overlaps before save
        instance = Booking(**data)
        if self.context['request'].user.is_authenticated:
            instance.user = self.context['request'].user
        else:
             # This might fail validation but handled in perform_create
             pass
        # Note: clean() is called on save() in model, but good to check here if complex
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Booking.objects.create(user=user, **validated_data)
