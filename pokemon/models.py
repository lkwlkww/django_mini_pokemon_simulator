from django.db import models

# Create your models here.
class Pokemon(models.Model):
    # Attributes found within csv
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=100)

    ## Randomly generated for a Pokemon upon its capture
    #level = models.IntegerField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
