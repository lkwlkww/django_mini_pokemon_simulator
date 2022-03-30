from django.urls import path,include

from django.views.decorators.csrf import csrf_exempt

from .views import AllPokemonView,UserPokemonView,AddPokemonView,ReleasePokemonView,UnownedPokemonView,CatchPokemonView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('allpokemon/', AllPokemonView.as_view()),
    path('unownedpokemon/', UnownedPokemonView.as_view()),
    path('mypokemon/', UserPokemonView.as_view()),
    path('addpokemon/', AddPokemonView.as_view(), name='addpokemon'),
    path('releasepokemon/', ReleasePokemonView.as_view()),
    #path('catchpokemon/', CatchPokemonView.as_view()),
    path('catchpokemon/', csrf_exempt(CatchPokemonView.as_view())),

]
