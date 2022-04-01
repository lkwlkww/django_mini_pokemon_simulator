from rest_framework import serializers

"""
This Serializer serializes various attributes of a Pokemon.
"""
class PokemonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    id = serializers.IntegerField()
    hp = serializers.IntegerField()
    attack = serializers.IntegerField()
    defense = serializers.IntegerField()
    type = serializers.CharField(max_length=100)

"""
This Serializer serializes the level and user of the captured pokemon, in addition to the serialized
fields in PokemonSerializer.
"""
class CapturedPokemonSerializer(PokemonSerializer):
    level = serializers.IntegerField()
    user = serializers.CharField(max_length=100)
