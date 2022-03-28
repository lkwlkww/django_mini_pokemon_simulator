from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from django.db import models

from .models import Pokemon, CapturedPokemon
from .serializers import PokemonSerializer, CapturedPokemonSerializer, WildPokemonSerializer

import random

'''
This view lists all the existing Pokemon.
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
This view lists all the captured pokemon of a user.
'''
class UserPokemonView(APIView):
    def get(self, request):
        # pokemon = CapturedPokemon.objects.filter(user=request.user)
        pokemon = CapturedPokemon.objects.all()
        serializer = CapturedPokemonSerializer(pokemon, many=True)
        return Response({'Captured Pokemon': serializer.data})

'''
This view is for adding a captured pokemon to a user's
repertoire of captured pokemon.
'''
class AddPokemonView(APIView):
    # permission_classes = (AllowAny,)
    """
    Get a randomly generated pokemon that has not been captured yet.
    """
    def get(self, request):
        wild_pokemon = Pokemon.objects.filter(captured=False)

        # get a random pokemon
        discovered_pokemon = random.choice(wild_pokemon)

        # set the discovered pokemon's level to a randomly generated int between 1 and 100
        discovered_pokemon.level = random.randint(1, 100)

        serializer = WildPokemonSerializer(discovered_pokemon)
        return Response({"Discovered wild pokemon": serializer.data})

    def post(self, request):
        pass

'''
This view is for listing all the pokemon that a user does not own.
'''
class UnownedPokemonView(APIView):
    def get(self, request):
        unowned_pokemon = Pokemon.objects.filter(user!=request.user)

        serializer = PokemonSerializer(unowned_pokemon)
        return Response({"Unowned pokemon": serializer.data})
