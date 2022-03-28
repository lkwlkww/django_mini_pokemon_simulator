from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from .models import Pokemon
from .serializers import PokemonSerializer

'''
This view lists all the existing Pokemon.
'''
class PokemonView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, pk):
        # pokemon = Pokemon.objects.values()
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        # return Response({'All existing Pokemon': pokemon})
        return Response({'Pokemon': serializer.data})

    def put(self, request, pk):
        saved_pokemon = get_object_or_404(Pokemon.objects.all(), pk=pk)
        data = request.data
        serializer = PokemonSerializer(instance=saved_pokemon, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            print('yes')
            pokemon_saved = serializer.save()
        return Response({'success': "Pokemon '{}' updated successfully".format(pokemon_saved.name)})

'''
This view allows a unique user to view all of his/her
captured Pokemon.
'''
class UserPokemonView(APIView):
    pass