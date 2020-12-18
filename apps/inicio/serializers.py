from rest_framework import serializers
from apps.inicio.models import *


class Prueba1Serializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    codigo = serializers.IntegerField()
    nombre = serializers.CharField()

    def create(self, validated_data):
        return Prueba.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre',instance.nombre)
        instance.save()
        return instance


class Prueba2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Prueba
        fields = ('codigo', 'nombre')


