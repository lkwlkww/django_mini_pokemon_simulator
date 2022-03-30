from django import forms
from django.core.exceptions import ValidationError

import random

'''
Form for catching a pokemon.
'''
class CatchPokemonForm(forms.Form):
    def __init__(self, *args, count=0, correct_num=random.randint(0,10), **kwargs):
        self.count = count
        self.correct_num = correct_num
        #self.count = kwargs.pop('count', 0) # Tracks the number of times a wrong number has been entered.
        #self.correct_num = correct_num
        # self.correct_num = random.randint(0,10) # The correct number that has to be guessed.
        super(CatchPokemonForm, self).__init__(*args, **kwargs)

    guess = forms.IntegerField(help_text="Enter a number between 0 and 10, inclusive.", required=True, initial=0, )
    Authorization_token = forms.CharField(max_length=1000)

    def clean(self):

        data = super(CatchPokemonForm, self).clean()
        data = data['guess']
        token = super(CatchPokemonForm, self).clean()['Authorization_token']
        print('correct num', self.correct_num)
        print('form count', self.count)
        print('token', token)

        # Attempt to catch pokemon fails, since there have been 3 wrong guesses.
        if self.count == 3:
            pass

        # Guess is lower than correct_num
        if data < self.correct_num:
            self.count += 1
            raise ValidationError('The answer is a larger number!', code='too_small')

        # Guess is larger than correct_num
        if data > self.correct_num:
            self.count += 1
            raise ValidationError('The answer is a smaller number!', code='too_large')
        return data
        
