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


#
# Serializer for the Django User table
#
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


    # Method for a custom update of the user table
    #
    # @param instance the instance of the user to update
    #
    # @param validated_data the params validated received in the request
    #
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
#
# Serializer class for the user's profile
#
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    profile_pic = Base64ImageField(
        max_length=None, required=False, use_url=True,
    )

    # Reference to the User table
    fk_user = UserSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserProfile
        fields = ('fk_user','fullname','game_points', 'profile_pic','country', 'city', 'badge')
        read_only_fields = ('game_points', 'badge')

    # This method overrides the creation of the profile, receiving the the data of the User table
    # and creating a token for the management of the user
    #
    # @param validated_data the params validated received in the request
    #
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

    # Method for a custom update of the user's profile table
    #
    # @param instance the instance of the user to update
    #
    # @param validated_data the params validated received in the request
    #
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

#
# Serializer for the tree reports in the Map
#
class TreePointSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    image = Base64ImageField(
        max_length=None, use_url=True, required=False,
    )

    # The user's profile picture
    profile_pic = Base64ImageField(
        max_length=None, use_url=True, required=False,
    )

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TreePoint
        fields = ('id', 'latitude','longitude','image', 'date', 'canopy', 'stem', 'height', 'type', 'location',
                  'status','user' , 'username', 'profile_pic','city')

    # This method creates a new tree point in the map
    # updates the state of the user's game profile and the stats of the city
    #
    # @param validated_data the params validated received in the request
    #
    def create(self,validated_data):
        green_point = TreePoint.objects.create(**validated_data)
        user = validated_data['user']
        status = validated_data['status']
        city = validated_data['city']

        # When the tree is reported by the user, automatically the status is unverified
        if (status==1):

            # Adding points tho the user
            cause = "Reporte Hecho"
            point_value = 2
            user.game_points += point_value
            user.save()

            # Update user badge
            updated_user = update_badge(user,point_value)

            # Add the game report
            game_report = GameReport(user=updated_user, cause=cause, point_status=green_point.status,point_value=point_value)
            game_report.save()

            # Update the quantity if the trees in the city reported
            city_exists = Stats.objects.filter(city=city).exists()
            if city_exists:
                stats = Stats.objects.get(city=city)
                stats.reported_trees += 1
                stats.save()
        return green_point

    # Method for a custom update of the TreePoint table
    #
    # @param instance the instance of the treepoint to update
    #
    # @param validated_data the params validated received in the request
    #
    def update(self, instance, validated_data):

        # The current status of the treepoint
        current_status = instance.status

        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.location = validated_data.get('location', instance.location)
        instance.type = validated_data.get('type', instance.type)
        instance.status = validated_data.get('status', instance.status)
        instance.user = validated_data.get('user', instance.user)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        # Update the game report
        user = validated_data['user']
        status = validated_data['status']
        cause = None
        point_value = 0

        # In the case of user request of red treepoint (space available to plant a tree)
        # from unrquested to requested
        if (status == 0):
            cause = "Solicitud Arbol"
            point_value = 5

        # In the case of tree validated (from unverified to verified)
        elif (status == 2):
            cause = "Reporte Verificado"
            point_value = 10

        # if the status is not verified and a admin updates de info
        if (current_status != 2):
            user.game_points += point_value
            user.save()
            updated_user = update_badge(user, point_value)
            game_report = GameReport(user=updated_user, cause=cause, point_status=status, point_value=point_value)
            game_report.save()

        return instance

# Method that updates the badge of the user in case of a change of game points
#
# @param user: the user who will receive a badge update
#
# @param points: the points of the event
#
def update_badge(user, points):

    # The points accumulated after the event
    count = user.game_points + points

    badges = Badge.objects.all()
    for badge in badges:
        # Check in the database the range of points in a badge and updates the user in
        # case of a level up
        if (badge.min_points <= count) and (count <= badge.max_points):
            user.badge = badge.badge_name
            user.save()
    return user


# Serializer for the rules of the game
class BadgeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Badge
        fields = ('badge_name','max_points','min_points')

# Serializer for the stats
class StatsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Stats
        fields = ('city','green_index','population_density','reported_trees')
        read_only = 'reported_trees'

# Serializer for the game reports
class GameReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameReport
        fields = ('user','cause','point_status','point_date','point_value')

# Serializer for the reported trees of the user
class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreePoint
        fields = ('status','type','location','date')

# Serializer for the stats of a particular city
class CityStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stats
        fields = ('city','green_index', 'population_density', 'reported_trees')

# Serializer for the user authentication
class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField() #password or token
    is_social = serializers.BooleanField()
    fullname = serializers.CharField()
    photo = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        is_social = attrs.get('is_social')
        fullname = attrs.get('fullname')
        photo = attrs.get('photo')

        print("estoy aqui"+str(is_social))
        if is_social:
            print("es social")
            if email and password:
                print("si hay email y pass")
                user_exists = User.objects.filter(email=email).exists()
                if user_exists:
                    print("existe user")
                    user = User.objects.get(email=email)
                    username = user.username
                    print("username"+username)
                    user_auth = authenticate(username=username, password=password)
                else:
                    username = generate_username(email)
                    user = User.objects.create(username=username, email=email)
                    user.set_password(password)
                    user.save()

                    print(str(fullname))

                    profile = UserProfile.objects.create(fk_user=user, fullname=str(fullname), social_token=password)
                    profile.save()
                    user_auth = authenticate(username=username, password=password)
            else:
                msg = "Unable to log in with provided credentials."
                raise exceptions.ValidationError(msg)
        else:

            if email and password:

                user_exists = User.objects.filter(email=email).exists()
                if user_exists:
                    user = User.objects.get(email=email)
                    username = user.username
                    user_auth = authenticate(username=username, password=password)
                else:

                    msg = "Unable to log in with provided credentials."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Must include email or username and password"
                raise exceptions.ValidationError(msg)

        attrs['user'] = user_auth
        return attrs

def generate_username(email):
    print("USER ID")
    # Get the list of user
    user_id_list = User.objects.all().order_by('-id')

    if user_id_list.count() > 0:
        highest_user_id = user_id_list[0].id
    else:
        highest_user_id = 0

    leading_part_of_email = email.split('@', 1)[0]
    #leading_part_of_email = re.sub(r'[^a-zA-Z0-9+]', '', leading_part_of_email)

    truncated_part_of_email = leading_part_of_email[:3] + leading_part_of_email[-3:]
    derived_username = truncated_part_of_email + str(highest_user_id + 1)

    return derived_username

# Serializer for the reset password
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            user = User.objects.filter(email=email)
            print(user)

        return attrs

# Serializer for the change of the password
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