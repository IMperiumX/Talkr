from rest_framework.routers import SimpleRouter

from network.api import views

router = SimpleRouter()

router.register("profile", views.ProfileViewSet)
router.register("post", views.PostViewSet)
router.register("postreaction", views.PostReactionViewSet)
router.register("retalk", views.RetalkViewSet)
router.register("postview", views.PostViewViewSet)
router.register("comment", views.CommentViewSet)
router.register("contact", views.ContactViewSet)

router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)

urlpatterns = router.urls
