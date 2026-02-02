from rest_framework import serializers
from django.utils.timesince import timesince
from .models import GovernmentResource, NewsArticle


class GovernmentResourceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = GovernmentResource
        fields = ['id', 'name', 'url', 'description', 'category', 'category_display', 'order']


class NewsArticleSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'description', 'source_name', 'url', 'image_url', 'published_at', 'time_ago']

    def get_time_ago(self, obj):
        return timesince(obj.published_at) + ' ago'
