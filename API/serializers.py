from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from rest_framework.generics import get_object_or_404
from .models import GreenPoint, UserProfile, Stats, Badge, User, GameReport

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
        fields = ('fk_user','fullname','game_points', 'profile_pic','country', 'city', 'badge')

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

class GreenPointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = GreenPoint
        fields = ('id', 'latitude','longitude','image', 'date', 'canopy', 'stem', 'height', 'type', 'location',
                  'status','user' , 'username')

    def create(self,validated_data):

        green_point = GreenPoint.objects.create(**validated_data)
        user = validated_data['user']
        status = validated_data['status']

        if (status==1):
            cause = "Reporte Hecho"
            point_value = 2
            user.game_points += point_value
            user.save()
            updated_user = update_badge(user,point_value)
            game_report = GameReport(user=updated_user, cause=cause, point_status=green_point.status,point_value=point_value)
            game_report.save()

        return green_point

    def update(self, instance, validated_data):
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.location = validated_data.get('location', instance.location)
        instance.type = validated_data.get('type', instance.type)
        instance.status = validated_data.get('status', instance.status)
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        user = validated_data['user']
        status = validated_data['status']

        if (status == 0):
            cause = "Solicitud Arbol"
            point_value = 5
            user.game_points += point_value
            user.save()
            updated_user = update_badge(user,point_value)
            game_report = GameReport(user=updated_user, cause=cause, point_status=status, point_value=point_value)
            game_report.save()

        return instance

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

class GameReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameReport
        fields = ('user','cause','point_status','point_date','point_value')


class RedPointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = GreenPoint
        fields = ('id','type','status','user')

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

def update_badge(user,points):

    count = user.game_points + points

    badges = Badge.objects.all()
    for badge in badges:
        if (badge.min_points <= count) and (count <= badge.max_points):
            user.badge = badge.badge_name
            user.save()
    return user
