from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CommentViewSet,
    BadgeViewSet,
    UserBadgeViewSet,
    PostLikeViewSet,
    UserRegistrationView,
    TripGroupViewSet,
    PostViewSet,
    GroupPostsView,
)
from .views import UserRegistrationView
router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'badges', BadgeViewSet)
router.register(r'user-badges', UserBadgeViewSet)
router.register(r'post-likes', PostLikeViewSet)
router.register(r'groups', TripGroupViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('groups/<int:group_id>/posts/', GroupPostsView.as_view(), name='group-posts'),
]
