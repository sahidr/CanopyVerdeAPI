from rest_framework import serializers
from .models import GreenPoint, UserProfile, Stats, Badge

class GreenPointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = GreenPoint
        fields = ('id', 'latitud','longitud','image', 'date', 'canopy', 'stem', 'height', 'type', 'location', 'status', 'user')

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserProfile
        fields = ('fullname','username','email', 'game_points', 'country', 'city')

class BadgeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Badge
        fields = ('badge_name','max_points','min_points')

class StatsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Stats
        fields = ('city','green_index','population_density')

