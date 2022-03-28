from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Pokemon(models.Model):
    # ATTRIBUTES # 
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class CapturedPokemon(Pokemon):
    level = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # List of pokemon captured by a user.
    captured_pokemon = []

    def __str__(self):
        return self.username
