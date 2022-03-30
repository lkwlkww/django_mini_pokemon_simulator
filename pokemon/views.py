from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

from django.db import models

from django.http import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt

from pokemon.forms import CatchPokemonForm

from .models import Pokemon
from .serializers import PokemonSerializer, CapturedPokemonSerializer

import random
import json


'''
This view outputs all the existing Pokemon through a GET request.
'''
class AllPokemonView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        return Response({'All existing Pokemon': serializer.data})

    """
    def put(self, request, pk):
        saved_pokemon = get_object_or_404(Pokemon.objects.all(), pk=pk)
        data = request.data
        serializer = PokemonSerializer(instance=saved_pokemon, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            pokemon_saved = serializer.save()
        return Response({'success': "Pokemon '{}' updated successfully".format(pokemon_saved.name)})
    """



'''
This view outputs all the captured pokemon of a user through a GET request.
'''
class UserPokemonView(APIView):
    # permission_classes = (AllowAny,)
    def get(self, request):
        # pokemon = CapturedPokemon.objects.filter(user=request.user)
        pokemon = Pokemon.objects.filter(captured=True).filter(user=request.user)
        serializer = CapturedPokemonSerializer(pokemon, many=True)
        return Response({'Captured Pokemon': serializer.data})

'''
This view is for adding a captured pokemon to a user's
repertoire of captured pokemon through a POST request. The input to the POST request
should contain the pokemon's name.
'''
class AddPokemonView(APIView):
    #permission_classes = (AllowAny,)

    def post(self, request):
        data = json.loads(request.body)
        pokemon_name = data['name']
        pokemon = get_object_or_404(Pokemon, name=pokemon_name)
        pokemon.user = request.user
        pokemon.captured = True
        pokemon.level = random.randint(1,100)
        pokemon.save()
        return HttpResponseRedirect('/pokemon/mypokemon')

'''
This view is for releasing a user's captured pokemon, through a POST request. The input to the
POST request should contain the pokemon's name.
'''
class ReleasePokemonView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        pokemon_name = data['name']
        pokemon = get_object_or_404(Pokemon, name=pokemon_name)
        pokemon.user = None
        pokemon.captured = False
        pokemon.level = None
        pokemon.save()
        return HttpResponseRedirect('/pokemon/mypokemon')

'''
This view is for listing all the pokemon that a user does not own, through a GET request.
'''
class UnownedPokemonView(APIView):
    def get(self, request):
        unowned_pokemon = Pokemon.objects.filter(~models.Q(user = request.user))

        serializer = PokemonSerializer(unowned_pokemon, many=True)
        return Response({"Unowned pokemon": serializer.data})
class LoginView(FormView):
    permission_classes = (AllowAny,) # This is set to allow anyone to access the page, so they can login.
    template_name = 'login.html'
    pass

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
class CatchPokemonView(FormView):
    #permission_classes = (AllowAny,)
    template_name = 'catch.html'
    success_url = 'pokemon/mypokemon/'

    wild_pokemon = random.choice(Pokemon.objects.filter(captured=False)) # Initialise a wild_pokemon that will be interacted with in the GET and POST methods.
    count = 0 # For tracking the number of guesses within an instance of the "guess the number" game.
    correct_num = random.randint(0, 10) # The correct answer for an instance of the "guess the number" game.

    def get(self ,request):
        print('get called')
        form = CatchPokemonForm()

        context = {
            'form': form,
            'pokemon': self.wild_pokemon,
        }

        print('token', request.GET.get('csrfmiddlewaretoken'))
        print(request.GET)
        return render(request, 'catch.html', context)

    def post(self, request):
        print('post', request.POST)
        print('POST called')
        print('view count', CatchPokemonView.count)
        CatchPokemonView.count += 1
        form = CatchPokemonForm(request.POST, count=CatchPokemonView.count, correct_num=self.correct_num)

        if form.is_valid(): # If guess is wrong, then ValidationError is raised which makes the form not valid.
            CatchPokemonView.count = 0
            self.catch(request.user)
            return HttpResponseRedirect(reverse('addpokemon'))
        else:
            if self.count == 3:
                #TODO: change to something that shows catch failed
                reset_game()
                return render(request, 'catch.html', {'form': form, 'pokemon': self.wild_pokemon})
            else:
                return render(request, 'catch.html', {'form': form, 'pokemon': self.wild_pokemon})

    def catch(self, user):
        #self.wild_pokemon.user = user 
        self.wild_pokemon.captured = True
        self.wild_pokemon.level = random.randint(1,100)
        self.wild_pokemon.save()

    def reset_game():
        CatchPokemonView.count = 0
        CatchPokemonView.correct_num = random.randint(0, 10)
        CatchPokemnoView.wild_pokemon = random.choice(Pokemon.objects.filter(captured=False))