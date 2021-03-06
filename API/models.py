from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Model of the user's profile
# Extended table for the Django User table
class UserProfile(models.Model):

    fk_user = models.OneToOneField(User, primary_key=True)
    fullname = models.CharField(max_length=60, blank=False)
    profile_pic = models.ImageField(upload_to='images/profile/', blank=True, default='images/logo.png', null=True)
    activation_key = models.CharField(max_length=50, blank=True)
    photo_loaded = models.BooleanField(default=False)
    country = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    game_points = models.IntegerField(blank=True,default=0)
    badge = models.CharField(max_length=100, blank=True, default="Apprentice")
    social_token = models.CharField(max_length=100, blank=True,null=True, default=None)

    def __str__(self):
        return self.fullname

class TreePoint(models.Model):

    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='images/tree/', blank=True, default=None, null=True)
    date = models.DateField(auto_now_add=True)
    canopy = models.IntegerField(blank=True, default=0)
    stem = models.IntegerField(blank=True, default=0)
    height = models.IntegerField(blank=True, default=0)
    type = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=255, blank=False)
    status = models.IntegerField(blank=False)
    user = models.ForeignKey(UserProfile, blank=True,default=None, null=True)
    city = models.CharField(max_length=100,default=None, null=True)

    def get_username(self):
        return self.user.fk_user.username

    username = property(get_username)

    def get_profile(self):
        return self.user.profile_pic

    profile_pic = property(get_profile)

    class Meta:
        unique_together = (('latitude', 'longitude'),)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return str(self.latitude)+','+str(self.longitude)


class Stats(models.Model):

    city = models.CharField(primary_key=True, max_length=100)
    green_index = models.FloatField(default=0)
    population_density = models.FloatField(default=0)
    reported_trees = models.IntegerField(default=0)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return self.city

class Badge(models.Model):

    badge_name = models.CharField(primary_key=True, max_length=50)
    max_points = models.IntegerField(unique=True)
    min_points = models.IntegerField(unique=True)

    class Meta:
        unique_together = (('max_points', 'min_points'),)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return self.badge_name

class GameReport(models.Model):
    user = models.ForeignKey(UserProfile)
    cause = models.CharField(max_length=60)
    point_status = models.IntegerField()
    point_date = models.DateField(auto_now_add=True)
    point_value = models.IntegerField()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return str(self.user)+str(self.cause)