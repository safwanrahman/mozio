from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .documents import ServiceAreaDocument
from .models import User, ServiceArea
from .serializers import UserSerializer, ServiceAreaSerializer


# Create your views here.


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ServiceAreaListView(generics.ListCreateAPIView):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # If its a get request, we should take the data from elasticsearch
        if self.request.method == "GET":
            return ServiceAreaDocument.search()
        else:
            return self.queryset

    def get_lat_lon(self):
        params = self.request.query_params
        lat = params.get("lat")
        lon = params.get("lon")
        if lat is None and lon is None:
            return lat, lon

        # Cast it to float in order to verify
        try:
            return float(lat), float(lon)
        except (ValueError, TypeError):
            return None, None

    def filter_queryset(self, queryset):
        lat, lon = self.get_lat_lon()
        if self.request.method == "GET" and lat is not None and lon is not None:
            query = ServiceAreaDocument.get_inside_query(lat=lat, lon=lon)
            queryset = queryset.filter(query)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = [obj.to_dict() for obj in page]
        serializer = self.get_serializer(data, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()
    permission_classes = [IsAuthenticated]
