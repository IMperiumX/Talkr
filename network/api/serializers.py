from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from network.models import (
    Comment,
    Contact,
    Post,
    PostReaction,
    PostView,
    Profile,
    Retalk,
)

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            "url",
            "name",
        ]


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"


class PostReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReaction
        fields = "__all__"


class RetalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Retalk
        fields = "__all__"


class PostViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostView
        fields = "__all__"


class MediaValidator:
    message = "Media file is too large"
    requires_context = True  # to access serializer field in __call__

    def __init__(self, max_size, message=None):
        self.max_size = max_size
        self.message = message or self.message

    def __call__(self, value, serializer_field):
        if value.size > self.max_size:
            raise serializers.ValidationError(self.message)
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # May be an anonymous user

    class Meta:
        model = Comment
        fields = ["id", "body", "media", "user"]
        validators = [
            MediaValidator(10 * 1024 * 1024),
        ]

    def create(self, validated_data):
        # Writable nested representations
        user_data = validated_data.pop("user")
        if user_data:
            user = User.objects.get_or_create(**user_data)
        comment = Comment.objects.create(user=user, **validated_data)
        comment.save()

    def update(self, instance, validated_data):
        # Update instance with validated data
        instance.body = validated_data.get("body", instance.body)
        instance.media = validated_data.get("media", instance.media)
        instance.save()
        return

    def validate_body(self, value):
        # If your body is declared with the parameter required=False
        # then this validation step will not take place if the field is not included
        if len(value) > 1000:
            raise serializers.ValidationError("Comment body is too long")
        return value


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ["user_from", "created", "user_to"]
        extra_kwargs = {
            "user_from": {
                "validators": [
                    serializers.UniqueTogetherValidator(
                        queryset=Contact.objects.all(),
                        fields=["user_from", "user_to"],
                        message="You already have a contact with this user",
                    )
                ]
            },
        }


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    liked_users = serializers.StringRelatedField(many=True)
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)
    reactions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="postreaction-detail",
        source="reactions_set",
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "body",
            "media",
            "total_likes",
            "status",
            "type",
            "published",
            "is_private",
            "author",
            "liked_users",
            "tags",
            "comments",
            "reactions",
        ]

    # Object-level validation
    def validate(self, data):
        from network.constants import DRAFT, PUBLISHED

        if data["status"] == DRAFT and data[PUBLISHED]:
            raise serializers.ValidationError(
                "Cannot set published status for draft post"
            )
        return data
