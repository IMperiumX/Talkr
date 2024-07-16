from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from network.api.serializers import (
    CommentSerializer,
    ContactSerializer,
    GroupSerializer,
    PostReactionSerializer,
    PostSerializer,
    PostViewSerializer,
    ProfileSerializer,
    RetalkSerializer,
    UserSerializer,
)
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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


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
