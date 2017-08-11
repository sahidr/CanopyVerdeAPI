from django.contrib.auth import authenticate, login
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404

from .models import GreenPoint, UserProfile, Stats, Badge, User

class GreenPointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = GreenPoint
        fields = ('id', 'latitude','longitude','image', 'date', 'canopy', 'stem', 'height', 'type', 'location',
                  'status','user' , 'username')

class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = ('id','username','email','password')

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    fk_user = UserSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserProfile
        fields = ('fk_user','fullname','game_points', 'profile_pic','country', 'city')

    def create(self, validated_data):
        user_data = validated_data.pop('fk_user')
        email = user_data['email']
        if (User.objects.filter(email=email).exists()):
            raise exceptions.ValidationError("User already created")
        else:
            fk_user = User(username=user_data['username'],email=email)
            fk_user.set_password(user_data['password'])
            fk_user.save()
            profile = UserProfile.objects.create(fk_user=fk_user, **validated_data)
            return profile


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

class AuthCustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Check if user sent email
            if authenticate_user(username):
                user_request = get_object_or_404(
                    User,
                    email=username,
                )
                username = user_request.username

            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = "User account is disabled."
                    raise exceptions.ValidationError(msg)
                #login(attrs,user)
            else:
                msg = "Unable to log in with provided credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must include email or username and password"
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

def authenticate_user(username=None):
    try:
        user = User.objects.get(username=username)
        if user is not None:
            return user
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username)
            if user is not None:
                return user
        except User.DoesNotExist:
            return None