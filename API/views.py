from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from .serializers import GreenPointSerializer, UserProfileSerializer, BadgeSerializer, StatsSerializer
from .models import GreenPoint, UserProfile, Stats, Badge

class CreateViewGreenPoint(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewGreenPoint(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer

class CreateViewUserProfile(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewUserProfile(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CreateViewBadge(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewBadge(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class CreateViewStats(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewStats(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
