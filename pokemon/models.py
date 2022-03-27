from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pokemon(models.Model):
    # Attributes found within csv
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=100)

    # Default level is 0. Changed to a randomly generated level from 0-100 upon a Pokemon's capture.
    level = models.IntegerField(default=0)

    ## The user that a Pokemon would belong to after it has been captured
    # user = models.ForeignKey(User)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
