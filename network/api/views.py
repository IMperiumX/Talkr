from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from network.models import (
    Comment,
    Contact,
    Post,
    PostReaction,
    PostView,
    Profile,
    Retalk,
)
from network.api.serializers import (
    CommentSerializer,
    ContactSerializer,
    PostReactionSerializer,
    PostSerializer,
    PostViewSerializer,
    ProfileSerializer,
    RetalkSerializer,
)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.order_by("pk")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.order_by("pk")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostReactionViewSet(ModelViewSet):
    queryset = PostReaction.objects.order_by("pk")
    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RetalkViewSet(ModelViewSet):
    queryset = Retalk.objects.order_by("pk")
    serializer_class = RetalkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewViewSet(ModelViewSet):
    queryset = PostView.objects.order_by("pk")
    serializer_class = PostViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.order_by("pk")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.order_by("pk")
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
