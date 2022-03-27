from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Pokemon

'''
This view allows us to view all the Pokemon in the Pokemon Universe.
'''
class PokemonView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        pokemon = Pokemon.objects.values()
        return Response({'All existing Pokemon': pokemon})

'''
This view allows a unique user to view all of his/her
captured Pokemon.
'''
class UserPokemonView(APIView):
    pass