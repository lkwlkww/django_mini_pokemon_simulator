from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Pokemon(models.Model):
    # ATTRIBUTES # 
    # Attributes found within the csv.
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=100)

    # Default level is 0. Changed to a randomly generated level from 0-100 upon a Pokemon's capture.
    level = models.IntegerField(default=0)

    # The user that a Pokemon would belong to after it has been captured
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    # METHODS

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class User(AbstractUser):
    # List of pokemon captured by a user.
    captured_pokemon = []

    def __str__(self):
        return self.username
