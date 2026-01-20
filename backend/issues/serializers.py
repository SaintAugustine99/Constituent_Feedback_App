from rest_framework import serializers
from .models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Auto-assign user from context
        user = self.context['request'].user
        return ServiceRequest.objects.create(user=user, **validated_data)
