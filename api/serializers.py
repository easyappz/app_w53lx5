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


# Ads domain serializers
class AdSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    source_url = serializers.URLField()
    title = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    image_url = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    published_at = serializers.DateTimeField(allow_null=True, required=False)
    category = serializers.CharField()
    view_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AdsQuerySerializer(serializers.Serializer):
    SORT_CHOICES = ("popular", "date")

    sort = serializers.ChoiceField(choices=SORT_CHOICES, required=False, default="popular")
    category = serializers.CharField(required=False, allow_blank=True)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=20)
    offset = serializers.IntegerField(required=False, min_value=0, default=0)


class ResolveSerializer(serializers.Serializer):
    url = serializers.URLField()


# Comments serializers
class CommentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    ad_id = serializers.CharField()
    username = serializers.CharField()
    text = serializers.CharField(min_length=1, max_length=2000)
    created_at = serializers.DateTimeField()


class CreateCommentSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=2000)
