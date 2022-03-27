from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils.translation import gettext as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
#from django.db.models import UserManager

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

    ## The user that a Pokemon would belong to after it has been captured
    # user = models.ForeignKey(User)

    # METHODS

    def __str__(self):
        return _(self.name)

    def __unicode__(self):
        return _(self.name)

class User(AbstractUser):
    captured_pokemon = []

    def __str__(self):
        return self.username
