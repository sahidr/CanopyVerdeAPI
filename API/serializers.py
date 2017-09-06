# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers, exceptions
from django.core.files.base import ContentFile
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import TreePoint, UserProfile, Stats, Badge, User, GameReport
import base64
import six
import uuid

#
# Class that process an Encode64 Image, this allows the ImageField to receive data instead a FILE
#
# Based on https://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file#28036805
#
class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            },
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user_exists = User.objects.filter(email=email).exists()
        current_email = instance.email
        if current_email != email:
            if not user_exists:
                instance.email = validated_data.get('email', instance.email)
                instance.save()
            else:
                content = {'code': 'email'}
                raise exceptions.ValidationError(content)
        if password != 'user_default_password_key':
            if len(str(password)) >= 8:
                instance.set_password(password)
                instance.save()
            else:
                content = {'code': 'password'}
                raise exceptions.ValidationError(content)
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    profile_pic = Base64ImageField(
        max_length=None, required=False, use_url=True,
    )

    fk_user = UserSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserProfile
        fields = ('fk_user','fullname','game_points', 'profile_pic','country', 'city', 'badge')
        read_only_fields = ('game_points', 'badge')

    def create(self, validated_data):
        user_data = validated_data.pop('fk_user')
        email = user_data['email']
        if (User.objects.filter(email=email).exists()):
            content = {'error':400}
            raise exceptions.ValidationError(content)
        else:
            fk_user = User(username=user_data['username'],email=email)
            fk_user.set_password(user_data['password'])
            fk_user.save()
            token, created = Token.objects.get_or_create(user=fk_user)
            profile = UserProfile.objects.create(fk_user=fk_user, activation_key=token, **validated_data)
            print(profile.activation_key)
            return profile

    def update(self, instance, validated_data):
        # A instance of a profile will be updated

        # Update a user
        user_data = validated_data.pop('fk_user')
        username = self.data['fk_user']['username']
        user = User.objects.get(username=username)
        user_serializer = UserSerializer(data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)

        # Update fields of UserProfile
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        return instance

class TreePointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    image = Base64ImageField(
        max_length=None, use_url=True, required=False,
    )

    profile_pic = Base64ImageField(
        max_length=None, use_url=True, required=False,
    )

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TreePoint
        fields = ('id', 'latitude','longitude','image', 'date', 'canopy', 'stem', 'height', 'type', 'location',
                  'status','user' , 'username', 'profile_pic','city')

    def create(self,validated_data):
        green_point = TreePoint.objects.create(**validated_data)
        user = validated_data['user']
        status = validated_data['status']
        city = validated_data['city']

        if (status==1):
            cause = "Reporte Hecho"
            point_value = 2
            user.game_points += point_value
            user.save()
            updated_user = update_badge(user,point_value)
            game_report = GameReport(user=updated_user, cause=cause, point_status=green_point.status,point_value=point_value)
            game_report.save()
            city_exists = Stats.objects.filter(city=city).exists()
            if city_exists:
                stats = Stats.objects.get(city=city)
                stats.reported_trees += 1
                stats.save()
        return green_point

    def update(self, instance, validated_data):

        current_status = instance.status

        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.location = validated_data.get('location', instance.location)
        instance.type = validated_data.get('type', instance.type)
        instance.status = validated_data.get('status', instance.status)
        instance.user = validated_data.get('user', instance.user)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        user = validated_data['user']
        status = validated_data['status']
        cause = None
        point_value = 0

        if (status == 0):
            cause = "Solicitud Arbol"
            point_value = 5
        elif (status == 2):
            cause = "Reporte Verificado"
            point_value = 10

        if (current_status != 2):
            user.game_points += point_value
            user.save()
            updated_user = update_badge(user, point_value)
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
        fields = ('city','green_index','population_density','reported_trees')
        read_only = 'reported_trees'

class GameReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameReport
        fields = ('user','cause','point_status','point_date','point_value')


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreePoint
        fields = ('status','type','location','date')

class RedPointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TreePoint
        fields = ('id','type','status','user')

class CityStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stats
        fields = ('city','green_index', 'population_density', 'reported_trees')

class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:

            user_exists = User.objects.filter(email=email).exists()
            if user_exists:
                user_email = User.objects.get(email=email)
                username = user_email.username
                user = authenticate(username=username, password=password)
            else:
                msg = "Unable to log in with provided credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must include email or username and password"
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

def update_badge(user,points):

    count = user.game_points + points

    badges = Badge.objects.all()
    for badge in badges:
        if (badge.min_points <= count) and (count <= badge.max_points):
            user.badge = badge.badge_name
            user.save()
    return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            user = User.objects.filter(email=email)
            print(user)

        return attrs

class ChangePasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = UserProfile
        fields = ('password','confirm_password','activation_key')
        extra_kwargs = {
            'activation_key': {'write_only': True},
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }