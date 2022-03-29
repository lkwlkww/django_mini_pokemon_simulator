from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions, mixins

from django.shortcuts import get_object_or_404, render,redirect

from django.db import models

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.edit import FormView

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
    # permission_classes = (AllowAny,)

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

'''
This view outputs a randomly generated pokemon for capture through a GET request.
'''
class CatchPokemonView(APIView):
    def get(self, request):
        wild_pokemon = Pokemon.objects.filter(captured=False)

        # get a random pokemon
        discovered_pokemon = random.choice(wild_pokemon)

        serializer = PokemonSerializer(discovered_pokemon)
        return Response({"Discovered wild pokemon": serializer.data})

"""
'''
Register API.
'''
class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Succesfully. Now perform Login to get your token",
        })
"""