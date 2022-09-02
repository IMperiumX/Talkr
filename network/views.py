from itertools import chain

from actions.utils import create_action
from common.decorators import ajax_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreatePostForm
from .models import Contact, Post

User = get_user_model()


# TODO: refactor (CBV & optimize iterable flatting logic)
@login_required
def following_posts(request, username):
    user = User.objects.get(username=username, is_active=True)
    user_to_set = user.following.all()
    following_post = [user.twitter_posts.all() for user in user_to_set]
    posts = list(chain.from_iterable(following_post))

    return render(request, "network/following.html", {"posts": posts})


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            status = form.cleaned_data["status"]
            user = request.user
            Post.objects.create(author=user, body=body, status=status)

        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/post_new.html", {"form": CreatePostForm()})


class UserDetailView(DetailView):
    model = User
    template_name = "user/detail.html"
    slug_url_kwarg = "username"
    slug_field = "username"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.twitter_posts.published()
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["date_of_birth", "photo", "username", "email"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get("id")
        is_liked = request.POST.get("is_liked")
        try:
            post = Post.objects.get(id=post_id)
            if is_liked == "no":
                post.users_like.add(request.user)
                is_liked = "yes"
            elif is_liked == "yes":
                post.users_like.remove(request.user)
                is_liked = "no"
            post.save()

            return JsonResponse(
                {
                    "like_count": post.users_like.count(),
                    "is_liked": is_liked,
                    "status": 201,
                }
            )
        except:
            return JsonResponse({"error": "Post not found", "status": 404})
    return JsonResponse({}, status=400)


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})


class PostListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    paginate_by = 10
    template_name = "network/index.html"


post_list_view = PostListView.as_view()


class PostDetailView(DetailView):
    model = Post
    template_name = "network/post_detail.html"


post_detail_view = PostDetailView.as_view()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "network/post_edit.html"
    fields = ["body", "status"]


post_update_view = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "network/post_delete.html"
    success_url = reverse_lazy("index")


post_delete_view = PostDeleteView.as_view()


class UserListView(ListView):
    queryset = User.objects.filter(is_active=True).exclude(id=1)
    paginate_by = 10
    context_object_name = "users"
    template_name = "user/list.html"


user_list_view = UserListView.as_view()
