from rest_framework import serializers
from .models import County, Constituency, Ward, Official

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['id', 'name', 'constituency']

class ConstituencySerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)
    
    class Meta:
        model = Constituency
        fields = ['id', 'name', 'county', 'wards']

class CountySerializer(serializers.ModelSerializer):
    constituencies = ConstituencySerializer(many=True, read_only=True)

    class Meta:
        model = County
        fields = ['id', 'name', 'code', 'constituencies']

class OfficialSerializer(serializers.ModelSerializer):
    title_display = serializers.CharField(source='get_title_display', read_only=True)
    class Meta:
        model = Official
        fields = '__all__'
