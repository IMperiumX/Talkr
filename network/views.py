from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Follow system packages.
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from actions.utils import create_action
from common.decorators import ajax_required
from .forms import CreatePostForm, ProfileEditForm, UserEditForm
from .models import Contact, Post


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

# TODO: Use CBV instead
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    posts = user.twitter_posts.all()
    return render(request, "user/detail.html", {"user": user, "posts": posts})


@login_required
def following_posts(request, username):
    user = User.objects.get(username=username, is_active=True)
    user_to_set = user.following.all()
    following_posts = [user.twitter_posts.all() for user in user_to_set]
    posts = list(chain.from_iterable(following_posts))

    return render(request, "network/following.html", {"posts": posts})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "network/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        is_liked = request.POST.get('is_liked')
        try:
            post = Post.objects.get(id=post_id)
            if is_liked == 'no':
                post.users_like.add(request.user)
                is_liked = 'yes'
            elif is_liked == 'yes':
                post.users_like.remove(request.user)
                is_liked = 'no'
            post.save()

            return JsonResponse(
                {
                    'like_count': post.users_like.count(),
                    'is_liked': is_liked,
                    "status": 201,
                }
            )
        except:
            return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 10
    template_name = "network/index.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "network/post_detail.html"


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "network/post_edit.html"
    fields = ["body", "status"]
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class PostDeleteView(DeleteView):
    model = Post
    template_name = "network/post_delete.html"
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404("You are not allowed to delete this Post")
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class UserPostListView(ListView):
    queryset = User.objects.filter(is_active=True).exclude(id=1)
    paginate_by = 10
    context_object_name = "users"
    template_name = "user/list.html"
