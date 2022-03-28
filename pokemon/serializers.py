from rest_framework import serializers

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
        instance.defense = validated_data.get('defesnse', instance.attack)
        instance.type = validated_data.get('type', instance.type)

        instance.save()
        return instance