from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
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


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = "__all__"


class PostReactionSerializer(ModelSerializer):

    class Meta:
        model = PostReaction
        fields = "__all__"


class RetalkSerializer(ModelSerializer):

    class Meta:
        model = Retalk
        fields = "__all__"


class PostViewSerializer(ModelSerializer):

    class Meta:
        model = PostView
        fields = "__all__"


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = "__all__"
