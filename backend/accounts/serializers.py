from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from locations.models import Ward, Constituency, County

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    # We accept IDs for the location, but we might want to validate them
    ward_id = serializers.IntegerField(required=True)

    def validate_password(self, value):
        django_validate_password(value)
        return value

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'ward_id']

    def create(self, validated_data):
        # Extract ward_id to handle relationship manually
        ward_id = validated_data.pop('ward_id')
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password) # Hashes the password
        
        try:
            ward = Ward.objects.get(id=ward_id)
            user.ward = ward
        except Ward.DoesNotExist:
            raise serializers.ValidationError({"ward_id": "Invalid Ward ID"})
            
        user.save()
        return user
