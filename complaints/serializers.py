from rest_framework import serializers
from .models import Complaint
from accounts.serializers import UserProfileSerializer

class ComplaintSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Complaint
        fields = ['id', 'user', 'title', 'description', 'commission_name', 'status', 'created_at']
        read_only_fields = ['created_at']

class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'commission_name']