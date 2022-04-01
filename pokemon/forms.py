from django import forms
from django.core.exceptions import ValidationError

from .models import Pokemon

import random

"""
This Form implements the "guess the number" game for catching a pokemon. Validation errors
are raised accordingly to if the guess is smaller or larger than the correct number. This flow
allows the software to give hints to the user, as part of the game.
"""
class AddPokemonForm(forms.Form):
    def __init__(self, *args, count=0, correct_num=random.randint(0,10), **kwargs):
        self.count = count # The number of guesses in an instance of the game.
        self.correct_num = correct_num # The correct number that has to be guessed.
        super(AddPokemonForm, self).__init__(*args, **kwargs)

    # The field where the user submits his/her guess.
    guess = forms.IntegerField(help_text="Enter a number between 0 and 10, inclusive.", required=True, initial=0, )

    def clean(self):
        data = super(AddPokemonForm, self).clean()
        data = data['guess']

        # Guess is lower than correct_num
        if data < self.correct_num:
            self.count += 1
            raise ValidationError('The answer is a larger number!')

        # Guess is larger than correct_num
        if data > self.correct_num:
            self.count += 1
            raise ValidationError('The answer is a smaller number!')

        return data

"""
This form implementns a UI that allows the user to submit the name of a captured pokemon
that he/she wishes to release.
"""
class ReleasePokemonForm(forms.Form):
    pokemon_name = forms.CharField(help_text="Enter the case-sensitive name of the pokemon to release.", required=True)

    def clean(self):
        data = super(ReleasePokemonForm, self).clean()
        pokemon_name = data['pokemon_name']
        try:
            pokemon = Pokemon.objects.get(name=pokemon_name)
        except Pokemon.DoesNotExist:
            pokemon = None

        # pokemon name cannot be found among the user's pokemon
        if pokemon == None:
            raise ValidationError("A pokemon of that name does not exist within your caught pokemon!")

        return data
