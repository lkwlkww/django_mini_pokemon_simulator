from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import random

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
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class User(AbstractUser):
    def __str__(self):
        return self.username

"""
    def create_captured_pokemon(self):
        # Updating captured field to reflect its capture.
        captured = True

        captured_pokemon = CapturedPokemon()
        captured_pokemon.level=random.randint(1, 100)
        self_fields = self._meta.get_fields()
        for field in captured_pokemon._meta.get_fields():
            field_name = field.name
            if field_name != 'level':
                if field_name in map(lambda x: x.name, self._meta.get_fields()):
                    setattr(captured_pokemon, field_name, getattr(self, field_name))
"""

"""
class CapturedPokemon(Pokemon):
    level = models.IntegerField()
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # List of pokemon captured by a user.
    # captured_pokemon = models.OneToManyField('CapturedPokemon')

    def __str__(self):
        return self.username
"""