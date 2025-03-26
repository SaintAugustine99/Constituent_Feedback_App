# feedback/serializers.py
from rest_framework import serializers
from .models import Category, Feedback, Response, Media
from accounts.serializers import UserProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent_category']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file_type', 'file_url', 'created_at']
        read_only_fields = ['created_at']

        def get_file_url(self, obj):
            if obj.file:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.file.url)
                return obj.file.url
            return None


class ResponseSerializer(serializers.ModelSerializer):
    responder = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Response
        fields = ['id', 'feedback', 'responder', 'content', 'created_at', 'is_public']
        read_only_fields = ['created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'title', 'description', 'category', 
            'sentiment_score', 'status', 'location_data', 
            'created_at', 'updated_at', 'is_public',
            'responses', 'media'
        ]
        read_only_fields = ['created_at', 'updated_at', 'sentiment_score']

class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['title', 'description', 'category', 'location_data', 'is_public']