from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse

from django.shortcuts import get_object_or_404, render, redirect
from django.db import models
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from .forms import AddPokemonForm, ReleasePokemonForm
from .models import Pokemon
from .serializers import PokemonSerializer, CapturedPokemonSerializer

import random
import json


'''
This view outputs all the existing Pokemon through a GET request.
'''
"""
This view displays all the pokemon that exist.
Methods:
get -   A GET request posted to this webpage causes a list of all existing
        pokemon to be displayed.
"""
class AllPokemonView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        return Response({'All existing Pokemon': serializer.data})

"""
This view displays a user's captured pokemon.
Methods:
get -   A GET request posted to this webpages causes a list of the user's captured
        pokemon to be displayed.
"""
class UserPokemonView(APIView):
    def get(self, request):
        pokemon = Pokemon.objects.filter(captured=True).filter(user=request.user)
        serializer = CapturedPokemonSerializer(pokemon, many=True)
        return Response({'Captured Pokemon': serializer.data})

"""
This view is for releasing a user's captured pokemon.
Methods:
get -   A GET request posted to this webpage causes this method to be called, which returns a render of the
        release.html file. The render shows a UI for submitting the case-sensitive name of the pokemon to be released.
post -  A POST request posted to the webpage causes this method to be called. If the request contains a name of a
        pokemon from the user's captured pokemon, then the attributes of the pokemon is changed to reflect that
        of a wild (uncaught) pokemon. Else, the release.html page is re-rendered and a statement telling the user
        that a captured pokemon of that name does not exist.
"""
class ReleasePokemonView(FormView):
    def get(self, request):
        form = ReleasePokemonForm()
        context = {
            'form': form,
        }
        return render(request, 'release.html', context)

    def post(self, request):
        form = ReleasePokemonForm(request.POST)
        if form.is_valid():
            pokemon_name = form.cleaned_data['pokemon_name']
            pokemon = Pokemon.objects.get(name=pokemon_name)
            pokemon.user = None
            pokemon.captured = False
            pokemon.level = None
            pokemon.save()
            return redirect(reverse('mypokemon'))
        else:
            return render(request, 'release.html', {'form': form})

"""
This view is for displaying all the pokemon that a user does not own.
Methods:
get -   A GET request posted to the webpage causes this method to be called, which displays
        a list of pokemon that the user does not own.
"""
class UnownedPokemonView(APIView):
    def get(self, request):
        unowned_pokemon = Pokemon.objects.filter(~models.Q(user = request.user))
        serializer = PokemonSerializer(unowned_pokemon, many=True)
        return Response({"Unowned pokemon": serializer.data})

"""
This view is for handling the catching of a pokemon.
Methods:
get -   A GET request posted to the webpage causes this method to be called, which returns
        a render of the catch.html file. The render shows a randomly generaated pokemon for
        capture, and a UI that implements the "guess the number" game.
post -  A POST request posted to the webpage causes this method to be called, of which what
        it returns depends on the results of the "guess the number" game. A wrong guess re-renders
        the page, three wrong guesses returns a redirect to a failure page, and a correct guess within
        three tries redirects the user to a page of his/her caught pokemon (updated with the
        pokemon that was just caught).
catch - Function to update the attributes of a caught pokemon to reflect its capture.
reset_game -    This function is called to reset the state of the game by generating new values for its random 
                attributes (wild_pokemon and correct_num), and resetting the count of guesses to 0.
"""
class AddPokemonView(FormView):
    wild_pokemon = random.choice(Pokemon.objects.filter(captured=False)) # Initialise a wild_pokemon that will be interacted with in the GET and POST methods.
    count = 0 # For tracking the number of guesses within an instance of the "guess the number" game.
    correct_num = random.randint(0, 10) # The correct answer for an instance of the "guess the number" game.

    def get(self ,request):
        form = AddPokemonForm()
        context = {
            'form': form,
            'pokemon': self.wild_pokemon,
        }
        return render(request, 'catch.html', context)

    def post(self, request):
        AddPokemonView.count += 1
        form = AddPokemonForm(request.POST, count=AddPokemonView.count, correct_num=self.correct_num)

        if form.is_valid(): # If guess is wrong, then ValidationError is raised which makes the form not valid.
            AddPokemonView.reset_game()
            self.catch(request.user)
            return redirect(reverse('mypokemon'))
        else:
            if self.count == 3: # Reset the game if 3 wrong tries have been made.
                AddPokemonView.reset_game()
            return render(request, 'catch.html', {'form': form, 'pokemon': self.wild_pokemon})

    def catch(self, user):
        self.wild_pokemon.user = user 
        self.wild_pokemon.captured = True
        self.wild_pokemon.level = random.randint(1,100)
        self.wild_pokemon.save()

    def reset_game():
        AddPokemonView.count = 0
        AddPokemonView.correct_num = random.randint(0, 10)
        AddPokemonView.wild_pokemon = random.choice(Pokemon.objects.filter(captured=False))