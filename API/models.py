from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your models here.

class UserProfile(models.Model):

    fk_user = models.OneToOneField(User, primary_key=True)
    fullname = models.CharField(max_length=60, blank=False)
    profile_pic = models.ImageField(upload_to='images/', blank=True, default=None, null=True)
    activation_key = models.CharField(max_length=40, blank=True)
    photo_loaded = models.BooleanField(default=False)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    game_points = models.IntegerField(blank=True,default=0)
    badge = models.CharField(max_length=100, blank=True, default="Apprentice")

    def __str__(self):
        return self.fullname

class GreenPoint(models.Model):

    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.URLField(blank=True)
    date = models.DateField(auto_now_add=True)
    canopy = models.IntegerField(blank=True, default=0)
    stem = models.IntegerField(blank=True, default=0)
    height = models.IntegerField(blank=True, default=0)
    type = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=255, blank=False)
    status = models.IntegerField(blank=False)
    user = models.ForeignKey(UserProfile, blank=True,default=None, null=True)

    def get_username(self):
        return self.user.fk_user.username

    username = property(get_username)

    def get_profile(self):
        return self.user.profile_pic

    #profile = property(get_profile)

    class Meta:
        unique_together = (('latitude', 'longitude'),)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return str(self.latitude)+','+str(self.longitude)


class Stats(models.Model):

    city = models.CharField(primary_key=True, max_length=100)
    green_index = models.IntegerField(default=0)
    population_density = models.IntegerField(default=0)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return self.city

class Badge(models.Model):

    badge_name = models.CharField(primary_key=True, max_length=50)
    max_points = models.IntegerField()
    min_points = models.IntegerField()

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