from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token

from .models import Pokemon, CapturedPokemon
from .serializers import PokemonSerializer, CapturedPokemonSerializer

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

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # pokemon = CapturedPokemon.objects.filter(user=request.user)
        pokemon = CapturedPokemon.objects.all()
        # token = Token.objects.get_or_create(user=request.user)
        print('yessssssssssssssssss')
        # print("token", token)
        serializer = CapturedPokemonSerializer(pokemon, many=True)
        return Response({'Captured Pokemon': serializer.data})
