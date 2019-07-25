from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from .models import User, ServiceArea


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "phone_number", "language", "currency"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user


class PolygonSerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField(child=serializers.ListField())

    def validate_type(self, value):
        value = value.lower()
        if value != "polygon":
            raise ValidationError("You can only add polygon type")

        return value


class ServiceAreaSerializer(serializers.ModelSerializer):
    area = PolygonSerializer(required=True)
    created_by = CharField(read_only=True)

    class Meta:
        model = ServiceArea
        fields = "__all__"

    def create(self, validated_data):
        obj = ServiceArea.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
