from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    timestamp = serializers.DateTimeField(read_only=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)


class MeSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
