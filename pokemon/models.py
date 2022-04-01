from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


"""
A model of a Pokemon.
"""
class Pokemon(models.Model):
    # ATTRIBUTES # 
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=100)
    captured = models.BooleanField(default=False)
    level = models.IntegerField(default=None, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=None, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

"""
A model of a User, as in the user that uses this software.
This class can be customised to make personalised changes to the User object for
various functionalities.
"""
class User(AbstractUser):
    def __str__(self):
        return self.username