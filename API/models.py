from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    #username = models.CharField(blank=True,max_length=60)
    #email = models.EmailField(primary_key=True)
    fk_user = models.OneToOneField(User, primary_key=True)
    fullname = models.CharField(max_length=60, blank=False)
    profile_pic = models.ImageField(upload_to='images/', blank=True)
    activation_key = models.CharField(max_length=40, blank=True)
    photo_loaded = models.BooleanField(default=False)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    game_points = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return self.fullname

class GreenPoint(models.Model):

    latitud = models.FloatField()
    longitud = models.FloatField()
    image = models.URLField(blank=True)
    date = models.DateField(auto_now_add=True)
    canopy = models.IntegerField(blank=True, default=0)
    stem = models.IntegerField(blank=True, default=0)
    height = models.IntegerField(blank=True, default=0)
    type = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=255, blank=False)
    status = models.IntegerField(blank=False)
    user = models.ForeignKey(UserProfile, blank=True,default=None, null=True)
    #user = models.EmailField(blank=False)

    class Meta:
        unique_together = (('latitud', 'longitud'),)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return str(self.latitud)+','+str(self.longitud)


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

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return self.badge_name