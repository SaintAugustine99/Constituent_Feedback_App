from rest_framework import generics, permissions
from .models import County, Constituency, Ward, Official
from .serializers import CountySerializer, ConstituencySerializer, WardSerializer, OfficialSerializer
from django.db import models

# 1. Get All Counties (Step 1 of Dropdown)
class CountyListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = County.objects.all()
    serializer_class = CountySerializer

# 2. Get Constituencies (Filtered by County)
class ConstituencyListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ConstituencySerializer

    def get_queryset(self):
        county_id = self.request.query_params.get('county_id')
        if county_id:
            return Constituency.objects.filter(county_id=county_id)
        return Constituency.objects.none() # Return nothing if no county selected

# 3. Get Wards (Filtered by Constituency)
class WardListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = WardSerializer

    def get_queryset(self):
        constituency_id = self.request.query_params.get('constituency_id')
        if constituency_id:
            return Ward.objects.filter(constituency_id=constituency_id)
        return Ward.objects.none()

class OfficialListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfficialSerializer

    def get_queryset(self):
        queryset = Official.objects.all()
        ward_id = self.request.query_params.get('ward_id')
        constituency_id = self.request.query_params.get('constituency_id')
        county_id = self.request.query_params.get('county_id')

        if ward_id:
            # Get MCA for this ward + MP for parent constituency + Governor/Senator for parent county
            # Ideally we filter by specific jurisdiction logic, but simpler approach:
            queryset = queryset.filter(models.Q(ward_id=ward_id) | models.Q(ward__isnull=True)) 
            # This is tricky without complex logic. Let's simplify: client sends specific jurisdiction IDs.
            pass
        
        # Simple exact match filters
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)
        if constituency_id:
            queryset = queryset.filter(constituency_id=constituency_id)
        if county_id:
            queryset = queryset.filter(county_id=county_id)
            
        return queryset
