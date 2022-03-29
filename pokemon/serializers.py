from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class PokemonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    id = serializers.IntegerField()
    hp = serializers.IntegerField()
    attack = serializers.IntegerField()
    defense = serializers.IntegerField()
    type = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.hp = validated_data.get('hp', instance.hp)
        instance.attack = validated_data.get('attack', instance.attack)
        instance.defense = validated_data.get('defense', instance.defense)
        instance.type = validated_data.get('type', instance.type)
        instance.level = validated_data.get('level', instance.level)

        instance.save()
        return instance

"""
Serializes the level and user of the captured pokemon, in addition to the serialized
fields in PokemonSerializer.
"""
class CapturedPokemonSerializer(PokemonSerializer):
    level = serializers.IntegerField()
    user = serializers.CharField(max_length=100)

"""
'''
Serializer to handle user registration.
'''
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name','last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

'''
Serializer to retrieve user values.
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
"""