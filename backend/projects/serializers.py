from rest_framework import serializers
from .models import Project, ProjectUpdate

class ProjectUpdateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ProjectUpdate
        fields = '__all__'
        read_only_fields = ['created_at', 'verified', 'user']

class ProjectSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source='ward.name', read_only=True)
    updates = ProjectUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
