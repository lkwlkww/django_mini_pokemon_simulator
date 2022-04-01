from django.urls import path,include

from .views import AllPokemonView,UserPokemonView,AddPokemonView,ReleasePokemonView,UnownedPokemonView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('allpokemon/', AllPokemonView.as_view(), name='allpokemon'),
    path('unownedpokemon/', UnownedPokemonView.as_view(), name='unownedpokemon'),
    path('mypokemon/', UserPokemonView.as_view(), name='mypokemon'),
    path('addpokemon/', AddPokemonView.as_view(), name='addpokemon'),
    path('releasepokemon/', ReleasePokemonView.as_view(), name='releasepokemon'),
]
