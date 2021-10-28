from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments', views.CommentViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments/(?P<comment_id>[^/.]+)', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token)
]

# urlpatterns = [
#     path("posts/", views.api_posts, name="api_posts"),
#     path("posts/<int:id>/", views.api_posts_detail, name="api_posts_detail"),
#     path("posts/api-token-auth/", obtain_auth_token),
# ]